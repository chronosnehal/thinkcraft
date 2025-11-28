#!/usr/bin/env python3
"""
Cryptocurrency Price Data Collection System - Solution Implementation

Description: Comprehensive system for fetching cryptocurrency price data from
public APIs and scraping additional market information, with robust error
handling, retry logic, timeout management, and data validation.

Time Complexity: O(n) where n = number of symbols/URLs
Space Complexity: O(m) where m = collected data size

Dependencies: Standard library (urllib, html.parser, json, csv, time, datetime)
Optional: requests, beautifulsoup4, lxml (for enhanced functionality)
Author: chronosnehal
Date: 2025-01-27
"""

from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse, urljoin, urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
from datetime import datetime, timezone
import json
import csv
import time
import logging
import re

# Try to import optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CryptocurrencyDataCollector:
    """
    Cryptocurrency price data collection system.
    
    This class provides methods for fetching cryptocurrency price data from
    public APIs, scraping additional market information, validating and
    normalizing data, and exporting results.
    
    Attributes:
        default_headers: Default HTTP headers
        last_request_time: Timestamp of last request (for rate limiting)
        api_providers: Supported API providers configuration
    """
    
    # API Provider configurations
    API_PROVIDERS = {
        "coingecko": {
            "base_url": "https://api.coingecko.com/api/v3",
            "price_endpoint": "/simple/price",
            "rate_limit": 1.0  # Minimum delay between requests (seconds)
        },
        "coincap": {
            "base_url": "https://api.coincap.io/v2",
            "price_endpoint": "/assets",
            "rate_limit": 0.3  # CoinCap allows faster requests
        }
    }
    
    def __init__(self, default_headers: Optional[Dict[str, str]] = None):
        """
        Initialize cryptocurrency data collector.
        
        Args:
            default_headers: Default HTTP headers to use for requests
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.default_headers = default_headers or {
            "User-Agent": "Mozilla/5.0 (compatible; CryptoDataCollector/1.0)",
            "Accept": "application/json"
        }
        self.last_request_time = 0.0
        
        logger.info("CryptocurrencyDataCollector initialized")
    
    def _validate_url(self, url: str) -> str:
        """
        Validate and normalize URL.
        
        Args:
            url: URL string to validate
        
        Returns:
            Normalized URL string
        
        Raises:
            ValueError: If URL is invalid
        """
        if not isinstance(url, str):
            raise TypeError("URL must be a string")
        
        if not url.strip():
            raise ValueError("URL cannot be empty")
        
        # Add protocol if missing
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        # Validate URL format
        parsed = urlparse(url)
        if not parsed.netloc:
            raise ValueError(f"Invalid URL format: {url}")
        
        return url
    
    def _apply_rate_limit(self, delay: float) -> None:
        """
        Apply rate limiting delay.
        
        Args:
            delay: Delay in seconds
        """
        if delay > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < delay:
                sleep_time = delay - elapsed
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _fetch_with_retry(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        retry_count: int = 3
    ) -> tuple[Optional[Dict[str, Any]], int, List[str]]:
        """
        Fetch data from URL with retry mechanism.
        
        Args:
            url: URL to fetch
            headers: HTTP headers
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts
        
        Returns:
            Tuple of (parsed_json_data, status_code, errors)
        """
        errors = []
        merged_headers = {**self.default_headers, **(headers or {})}
        
        for attempt in range(retry_count + 1):
            try:
                if REQUESTS_AVAILABLE:
                    response = requests.get(
                        url,
                        headers=merged_headers,
                        timeout=timeout,
                        allow_redirects=True
                    )
                    
                    # Handle rate limiting (429)
                    if response.status_code == 429:
                        if attempt < retry_count:
                            wait_time = 2 ** attempt
                            logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            continue
                    
                    response.raise_for_status()
                    return response.json(), response.status_code, errors
                else:
                    # Use urllib from standard library
                    request = Request(url, headers=merged_headers)
                    with urlopen(request, timeout=timeout) as response:
                        content = response.read().decode('utf-8', errors='ignore')
                        status_code = response.getcode()
                        
                        if status_code == 429:
                            if attempt < retry_count:
                                wait_time = 2 ** attempt
                                logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                                time.sleep(wait_time)
                                continue
                        
                        try:
                            parsed_data = json.loads(content)
                            return parsed_data, status_code, errors
                        except json.JSONDecodeError as e:
                            error_msg = f"JSON decode error: {str(e)}"
                            errors.append(error_msg)
                            return None, status_code, errors
            
            except HTTPError as e:
                status_code = e.code
                error_msg = f"HTTP error {status_code}: {e.reason}"
                errors.append(f"{error_msg} (attempt {attempt + 1})")
                
                if status_code in [404, 403, 401]:
                    # Don't retry for these status codes
                    logger.error(error_msg)
                    return None, status_code, errors
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, status_code, errors
            
            except URLError as e:
                error_msg = f"URL error: {str(e)}"
                errors.append(f"{error_msg} (attempt {attempt + 1})")
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, 0, errors
            
            except json.JSONDecodeError as e:
                error_msg = f"JSON decode error: {str(e)}"
                errors.append(f"{error_msg} (attempt {attempt + 1})")
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, 0, errors
            
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                errors.append(f"{error_msg} (attempt {attempt + 1})")
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, 0, errors
        
        return None, 0, errors
    
    def _fetch_page(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        retry_count: int = 3
    ) -> tuple[Optional[str], int, List[str]]:
        """
        Fetch web page with retry mechanism.
        
        Args:
            url: URL to fetch
            headers: HTTP headers
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts
        
        Returns:
            Tuple of (content, status_code, errors)
        """
        errors = []
        merged_headers = {**self.default_headers, **(headers or {})}
        
        for attempt in range(retry_count + 1):
            try:
                if REQUESTS_AVAILABLE:
                    response = requests.get(
                        url,
                        headers=merged_headers,
                        timeout=timeout,
                        allow_redirects=True
                    )
                    response.raise_for_status()
                    return response.text, response.status_code, errors
                else:
                    request = Request(url, headers=merged_headers)
                    with urlopen(request, timeout=timeout) as response:
                        content = response.read().decode('utf-8', errors='ignore')
                        status_code = response.getcode()
                        return content, status_code, errors
            
            except HTTPError as e:
                status_code = e.code
                error_msg = f"HTTP error {status_code}: {e.reason}"
                errors.append(error_msg)
                
                if status_code in [404, 403, 401]:
                    logger.error(error_msg)
                    return None, status_code, errors
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, status_code, errors
            
            except URLError as e:
                error_msg = f"URL error: {str(e)}"
                errors.append(error_msg)
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, 0, errors
            
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                errors.append(error_msg)
                
                if attempt < retry_count:
                    wait_time = 2 ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retry_count + 1} attempts: {error_msg}")
                    return None, 0, errors
        
        return None, 0, errors
    
    def _parse_coingecko_response(
        self,
        data: Dict[str, Any],
        symbols: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Parse CoinGecko API response.
        
        Args:
            data: API response JSON
            symbols: List of requested symbols
        
        Returns:
            List of parsed cryptocurrency data dictionaries
        """
        results = []
        
        for symbol in symbols:
            if symbol not in data:
                continue
            
            coin_data = data[symbol]
            result = {
                "symbol": symbol,
                "name": symbol.capitalize(),  # CoinGecko uses IDs, not names
                "price_usd": coin_data.get("usd"),
                "market_cap_usd": coin_data.get("usd_market_cap"),
                "volume_24h_usd": coin_data.get("usd_24h_vol"),
                "price_change_24h_percent": coin_data.get("usd_24h_change"),
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            results.append(result)
        
        return results
    
    def _parse_coincap_response(
        self,
        data: Dict[str, Any],
        symbols: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Parse CoinCap API response.
        
        Args:
            data: API response JSON
            symbols: List of requested symbols
        
        Returns:
            List of parsed cryptocurrency data dictionaries
        """
        results = []
        
        if "data" not in data:
            return results
        
        # CoinCap returns list of assets
        assets = data["data"]
        
        # Map CoinCap IDs to our symbols (simplified - in practice, need proper mapping)
        symbol_map = {symbol.lower(): symbol.lower() for symbol in symbols}
        
        for asset in assets:
            asset_id = asset.get("id", "").lower()
            if asset_id in symbol_map:
                result = {
                    "symbol": asset_id,
                    "name": asset.get("name", asset_id),
                    "price_usd": float(asset.get("priceUsd", 0)) if asset.get("priceUsd") else None,
                    "market_cap_usd": float(asset.get("marketCapUsd", 0)) if asset.get("marketCapUsd") else None,
                    "volume_24h_usd": float(asset.get("volumeUsd24Hr", 0)) if asset.get("volumeUsd24Hr") else None,
                    "price_change_24h_percent": float(asset.get("changePercent24Hr", 0)) if asset.get("changePercent24Hr") else None,
                    "last_updated": asset.get("timestamp", datetime.now(timezone.utc).isoformat())
                }
                results.append(result)
        
        return results
    
    def fetch_crypto_prices(
        self,
        symbols: List[str],
        api_provider: str = "coingecko",
        include_market_data: bool = True,
        timeout: int = 10,
        retry_count: int = 3,
        rate_limit: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Fetch cryptocurrency price data from public API.
        
        Args:
            symbols: List of cryptocurrency symbols (e.g., ["bitcoin", "ethereum"])
            api_provider: API provider ("coingecko" or "coincap")
            include_market_data: Include market cap, volume, etc.
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts
            rate_limit: Delay between requests in seconds (uses provider default if None)
        
        Returns:
            Dictionary with price data and metadata
        
        Raises:
            ValueError: If symbols is empty or provider is invalid
            TypeError: If inputs have wrong types
        
        Time Complexity: O(n) where n = number of symbols
        Space Complexity: O(n) where n = number of symbols
        
        Examples:
            >>> collector = CryptocurrencyDataCollector()
            >>> result = collector.fetch_crypto_prices(["bitcoin", "ethereum"])
            >>> print(result["data"][0]["price_usd"])
        """
        start_time = time.time()
        
        # Validate inputs
        if not isinstance(symbols, list) or not symbols:
            raise ValueError("Symbols must be a non-empty list")
        
        if not all(isinstance(s, str) for s in symbols):
            raise TypeError("All symbols must be strings")
        
        if api_provider not in self.API_PROVIDERS:
            raise ValueError(f"Invalid API provider. Must be one of: {list(self.API_PROVIDERS.keys())}")
        
        if timeout < 1 or timeout > 60:
            raise ValueError("Timeout must be between 1 and 60 seconds")
        
        if retry_count < 0 or retry_count > 10:
            raise ValueError("Retry count must be between 0 and 10")
        
        provider_config = self.API_PROVIDERS[api_provider]
        delay = rate_limit if rate_limit is not None else provider_config["rate_limit"]
        
        logger.info(f"Fetching prices for {len(symbols)} symbols from {api_provider}")
        
        # Apply rate limiting
        self._apply_rate_limit(delay)
        
        # Build API URL
        if api_provider == "coingecko":
            # CoinGecko API
            ids = ",".join(symbols)
            params = {
                "ids": ids,
                "vs_currencies": "usd"
            }
            if include_market_data:
                params["include_market_cap"] = "true"
                params["include_24hr_vol"] = "true"
                params["include_24hr_change"] = "true"
            
            url = f"{provider_config['base_url']}{provider_config['price_endpoint']}?{urlencode(params)}"
        else:
            # CoinCap API
            ids = ",".join(symbols)
            url = f"{provider_config['base_url']}{provider_config['price_endpoint']}?ids={ids}"
        
        # Fetch data
        data, status_code, errors = self._fetch_with_retry(
            url=url,
            timeout=timeout,
            retry_count=retry_count
        )
        
        fetch_time = time.time() - start_time
        
        if data is None:
            return {
                "success": False,
                "source": api_provider,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": [],
                "metadata": {
                    "total_symbols": len(symbols),
                    "successful_fetches": 0,
                    "failed_fetches": len(symbols),
                    "fetch_time": round(fetch_time, 2)
                },
                "errors": errors,
                "warnings": []
            }
        
        # Parse response based on provider
        if api_provider == "coingecko":
            parsed_data = self._parse_coingecko_response(data, symbols)
        else:
            parsed_data = self._parse_coincap_response(data, symbols)
        
        successful = len(parsed_data)
        failed = len(symbols) - successful
        
        logger.info(
            f"Fetched prices: {successful} successful, {failed} failed, "
            f"time: {fetch_time:.2f}s"
        )
        
        return {
            "success": successful > 0,
            "source": api_provider,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": parsed_data,
            "metadata": {
                "total_symbols": len(symbols),
                "successful_fetches": successful,
                "failed_fetches": failed,
                "fetch_time": round(fetch_time, 2)
            },
            "errors": errors,
            "warnings": [f"Symbol '{s}' not found" for s in symbols if s not in [d["symbol"] for d in parsed_data]]
        }
    
    def scrape_market_info(
        self,
        url: str,
        selectors: Dict[str, Union[str, Dict[str, str]]],
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        retry_count: int = 3,
        rate_limit: float = 1.0
    ) -> Dict[str, Any]:
        """
        Scrape additional market information from web source.
        
        Args:
            url: URL to scrape
            selectors: Dictionary mapping field names to CSS selectors
            headers: Optional HTTP headers
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts
            rate_limit: Delay between requests in seconds
        
        Returns:
            Dictionary with scraped data and metadata
        
        Raises:
            ValueError: If URL is invalid or selectors are empty
            TypeError: If inputs have wrong types
        
        Time Complexity: O(n) where n = HTML content size
        Space Complexity: O(m) where m = extracted data size
        """
        start_time = time.time()
        
        # Validate inputs
        if not isinstance(selectors, dict) or not selectors:
            raise ValueError("Selectors must be a non-empty dictionary")
        
        url = self._validate_url(url)
        
        logger.info(f"Scraping market info from: {url}")
        
        # Apply rate limiting
        self._apply_rate_limit(rate_limit)
        
        # Fetch page
        content, status_code, errors = self._fetch_page(
            url=url,
            headers=headers,
            timeout=timeout,
            retry_count=retry_count
        )
        
        if content is None:
            return {
                "success": False,
                "url": url,
                "data": {},
                "metadata": {
                    "status_code": status_code,
                    "scraping_time": round(time.time() - start_time, 2),
                    "elements_found": {}
                },
                "errors": errors,
                "warnings": []
            }
        
        # Parse HTML
        parsed_html = self._parse_html(content)
        
        # Extract data
        data = {}
        elements_found = {}
        warnings = []
        
        for field_name, selector_config in selectors.items():
            try:
                if isinstance(selector_config, dict):
                    nested_data = {}
                    for nested_field, nested_selector in selector_config.items():
                        result = self._extract_with_selector(parsed_html, nested_selector, multiple=False)
                        nested_data[nested_field] = result
                        elements_found[f"{field_name}.{nested_field}"] = 1 if result else 0
                    data[field_name] = nested_data
                else:
                    selector_str = str(selector_config)
                    multiple = field_name.endswith("s") or "list" in field_name.lower()
                    
                    result = self._extract_with_selector(parsed_html, selector_str, multiple=multiple)
                    data[field_name] = result
                    
                    if isinstance(result, list):
                        elements_found[field_name] = len(result)
                    else:
                        elements_found[field_name] = 1 if result else 0
                    
                    if result is None or (isinstance(result, list) and len(result) == 0):
                        warnings.append(f"No elements found for selector '{field_name}': {selector_str}")
            
            except Exception as e:
                error_msg = f"Error extracting '{field_name}': {str(e)}"
                warnings.append(error_msg)
                logger.warning(error_msg)
                data[field_name] = None
                elements_found[field_name] = 0
        
        scraping_time = time.time() - start_time
        
        logger.info(
            f"Scraping completed: {len(data)} fields extracted, "
            f"{len(warnings)} warnings, time: {scraping_time:.2f}s"
        )
        
        return {
            "success": True,
            "url": url,
            "data": data,
            "metadata": {
                "status_code": status_code,
                "scraping_time": round(scraping_time, 2),
                "elements_found": elements_found
            },
            "errors": errors,
            "warnings": warnings
        }
    
    def _parse_html(self, html_content: str) -> Any:
        """
        Parse HTML content.
        
        Args:
            html_content: HTML content string
        
        Returns:
            Parsed HTML object (BeautifulSoup if available, else raw HTML)
        """
        if BS4_AVAILABLE:
            return BeautifulSoup(html_content, 'html.parser')
        else:
            return html_content
    
    def _extract_with_selector(
        self,
        parsed_html: Any,
        selector: str,
        multiple: bool = False
    ) -> Union[str, List[str], None]:
        """
        Extract data using CSS selector.
        
        Args:
            parsed_html: Parsed HTML object
            selector: CSS selector or XPath
            multiple: Whether to extract multiple elements
        
        Returns:
            Extracted text or list of texts
        """
        if parsed_html is None:
            return None if not multiple else []
        
        extract_attr = None
        if "::" in selector:
            selector, extract_attr = selector.split("::", 1)
        
        try:
            if BS4_AVAILABLE:
                elements = parsed_html.select(selector)
                
                if not elements:
                    return None if not multiple else []
                
                if extract_attr:
                    if multiple:
                        return [elem.get(extract_attr, "") for elem in elements if elem.get(extract_attr)]
                    else:
                        return elements[0].get(extract_attr, "") if elements else None
                else:
                    if multiple:
                        return [elem.get_text(strip=True) for elem in elements]
                    else:
                        return elements[0].get_text(strip=True) if elements else None
            else:
                logger.warning("BeautifulSoup not available, using basic extraction")
                if extract_attr:
                    pattern = rf'<{selector.split(".")[0]}[^>]*{extract_attr}="([^"]*)"'
                    matches = re.findall(pattern, str(parsed_html))
                    return matches if multiple else (matches[0] if matches else None)
                else:
                    pattern = rf'<{selector}[^>]*>(.*?)</{selector}>'
                    matches = re.findall(pattern, str(parsed_html), re.DOTALL)
                    if matches:
                        cleaned = [re.sub(r'<[^>]+>', '', m).strip() for m in matches]
                        return cleaned if multiple else cleaned[0]
                    return None if not multiple else []
        
        except Exception as e:
            logger.warning(f"Error extracting with selector '{selector}': {e}")
            return None if not multiple else []
    
    def validate_data(
        self,
        data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate collected cryptocurrency data for consistency and completeness.
        
        Args:
            data: List of cryptocurrency data dictionaries
        
        Returns:
            Dictionary with validation report and validated data
        
        Time Complexity: O(n) where n = number of records
        Space Complexity: O(n) where n = number of records
        """
        start_time = time.time()
        
        validated_data = []
        missing_fields = []
        complete_records = 0
        incomplete_records = 0
        
        required_fields = ["symbol", "price_usd"]
        optional_fields = ["market_cap_usd", "volume_24h_usd", "price_change_24h_percent"]
        
        for record in data:
            validated_record = record.copy()
            record_missing = []
            is_complete = True
            
            # Check required fields
            for field in required_fields:
                if field not in record or record[field] is None:
                    record_missing.append(f"{record.get('symbol', 'unknown')}.{field}")
                    is_complete = False
                else:
                    # Validate data types
                    if field == "price_usd":
                        try:
                            validated_record[field] = float(record[field])
                            if validated_record[field] <= 0:
                                record_missing.append(f"{record.get('symbol', 'unknown')}.{field} (invalid)")
                                is_complete = False
                        except (ValueError, TypeError):
                            record_missing.append(f"{record.get('symbol', 'unknown')}.{field} (type_error)")
                            is_complete = False
            
            # Check optional fields and normalize
            for field in optional_fields:
                if field in record and record[field] is not None:
                    try:
                        value = float(record[field])
                        if field in ["market_cap_usd", "volume_24h_usd"] and value < 0:
                            validated_record[field] = None
                            record_missing.append(f"{record.get('symbol', 'unknown')}.{field} (negative)")
                        else:
                            validated_record[field] = value
                    except (ValueError, TypeError):
                        validated_record[field] = None
                        record_missing.append(f"{record.get('symbol', 'unknown')}.{field} (type_error)")
            
            validated_record["is_complete"] = is_complete
            
            if is_complete:
                complete_records += 1
            else:
                incomplete_records += 1
            
            missing_fields.extend(record_missing)
            validated_data.append(validated_record)
        
        # Consistency checks
        consistency_passed = True
        if len(validated_data) > 1:
            # Check if all records have consistent structure
            first_keys = set(validated_data[0].keys())
            for record in validated_data[1:]:
                if set(record.keys()) != first_keys:
                    consistency_passed = False
                    break
        
        validation_time = time.time() - start_time
        
        logger.info(
            f"Validation completed: {complete_records} complete, "
            f"{incomplete_records} incomplete, time: {validation_time:.2f}s"
        )
        
        return {
            "validated_data": validated_data,
            "validation_report": {
                "total_records": len(data),
                "complete_records": complete_records,
                "incomplete_records": incomplete_records,
                "consistency_checks_passed": consistency_passed,
                "missing_fields": list(set(missing_fields))  # Remove duplicates
            },
            "validation_time": round(validation_time, 2)
        }
    
    def collect_crypto_data(
        self,
        symbols: List[str],
        fetch_api_data: bool = True,
        scrape_market_info: bool = False,
        scrape_urls: Optional[List[str]] = None,
        scrape_selectors: Optional[Dict[str, Union[str, Dict[str, str]]]] = None,
        validate_data: bool = True,
        api_provider: str = "coingecko",
        timeout: int = 10,
        retry_count: int = 3,
        rate_limit: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Collect cryptocurrency data from APIs and web sources.
        
        Args:
            symbols: List of cryptocurrency symbols
            fetch_api_data: Fetch from API (default: True)
            scrape_market_info: Scrape web sources (default: False)
            scrape_urls: URLs to scrape for additional info
            scrape_selectors: Selectors for web scraping
            validate_data: Validate collected data (default: True)
            api_provider: API provider ("coingecko" or "coincap")
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts
            rate_limit: Delay between requests in seconds
        
        Returns:
            Dictionary with collected and validated data
        
        Raises:
            ValueError: If inputs are invalid
        
        Time Complexity: O(n + m) where n = symbols, m = URLs
        Space Complexity: O(k) where k = collected data size
        """
        start_time = time.time()
        all_errors = []
        all_warnings = []
        
        api_data = None
        scraped_data = []
        
        # Fetch API data
        if fetch_api_data:
            try:
                api_data = self.fetch_crypto_prices(
                    symbols=symbols,
                    api_provider=api_provider,
                    timeout=timeout,
                    retry_count=retry_count,
                    rate_limit=rate_limit
                )
                all_errors.extend(api_data.get("errors", []))
                all_warnings.extend(api_data.get("warnings", []))
            except Exception as e:
                error_msg = f"API fetch failed: {str(e)}"
                all_errors.append(error_msg)
                logger.error(error_msg)
        
        # Scrape web data
        if scrape_market_info and scrape_urls and scrape_selectors:
            for url in scrape_urls:
                try:
                    scraped_result = self.scrape_market_info(
                        url=url,
                        selectors=scrape_selectors,
                        timeout=timeout,
                        retry_count=retry_count,
                        rate_limit=rate_limit or 1.0
                    )
                    scraped_data.append(scraped_result)
                    all_errors.extend(scraped_result.get("errors", []))
                    all_warnings.extend(scraped_result.get("warnings", []))
                except Exception as e:
                    error_msg = f"Scraping failed for {url}: {str(e)}"
                    all_errors.append(error_msg)
                    logger.error(error_msg)
        
        # Validate data
        validated_data = None
        validation_report = None
        
        if validate_data and api_data and api_data.get("success"):
            validation_result = self.validate_data(api_data["data"])
            validated_data = validation_result["validated_data"]
            validation_report = validation_result["validation_report"]
        
        total_time = time.time() - start_time
        
        # Calculate individual times
        api_fetch_time = api_data.get("metadata", {}).get("fetch_time", 0) if api_data else 0
        scraping_time = sum(s.get("metadata", {}).get("scraping_time", 0) for s in scraped_data)
        validation_time = validation_result.get("validation_time", 0) if validate_data and api_data else 0
        
        logger.info(
            f"Collection completed: total time {total_time:.2f}s, "
            f"API: {api_fetch_time:.2f}s, Scraping: {scraping_time:.2f}s, "
            f"Validation: {validation_time:.2f}s"
        )
        
        return {
            "success": (api_data and api_data.get("success")) or len(scraped_data) > 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "api_data": api_data,
            "scraped_data": scraped_data,
            "validated_data": validated_data,
            "validation_report": validation_report,
            "metadata": {
                "total_collection_time": round(total_time, 2),
                "api_fetch_time": round(api_fetch_time, 2),
                "scraping_time": round(scraping_time, 2),
                "validation_time": round(validation_time, 2)
            },
            "errors": all_errors,
            "warnings": all_warnings
        }
    
    def export_to_json(self, data: Dict[str, Any], filename: str) -> None:
        """
        Export collected data to JSON file.
        
        Args:
            data: Data dictionary
            filename: Output filename
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def export_to_csv(self, data: Dict[str, Any], filename: str) -> None:
        """
        Export collected data to CSV file.
        
        Args:
            data: Data dictionary
            filename: Output filename
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            # Extract records from validated_data or api_data
            records = []
            if "validated_data" in data and data["validated_data"]:
                records = data["validated_data"]
            elif "api_data" in data and data["api_data"] and "data" in data["api_data"]:
                records = data["api_data"]["data"]
            elif "data" in data:
                records = data["data"] if isinstance(data["data"], list) else [data["data"]]
            
            if not records:
                logger.warning("No records to export to CSV")
                return
            
            # Get all field names
            fieldnames = set()
            for record in records:
                fieldnames.update(record.keys())
            fieldnames = sorted(fieldnames)
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise


def main():
    """Demonstrate cryptocurrency data collection with examples."""
    collector = CryptocurrencyDataCollector()
    
    print("=" * 80)
    print("Cryptocurrency Price Data Collection System - Examples")
    print("=" * 80)
    
    # Example 1: Fetch Bitcoin price from API
    print("\n" + "-" * 80)
    print("Example 1: Fetch Bitcoin Price from CoinGecko API")
    print("-" * 80)
    
    try:
        result1 = collector.fetch_crypto_prices(
            symbols=["bitcoin"],
            api_provider="coingecko",
            include_market_data=True
        )
        
        if result1["success"] and result1["data"]:
            bitcoin_data = result1["data"][0]
            print(f"✓ Successfully fetched Bitcoin price")
            print(f"  Symbol: {bitcoin_data.get('symbol')}")
            print(f"  Price (USD): ${bitcoin_data.get('price_usd', 'N/A')}")
            print(f"  Market Cap: ${bitcoin_data.get('market_cap_usd', 'N/A'):,.0f}" if bitcoin_data.get('market_cap_usd') else "  Market Cap: N/A")
            print(f"  24h Volume: ${bitcoin_data.get('volume_24h_usd', 'N/A'):,.0f}" if bitcoin_data.get('volume_24h_usd') else "  24h Volume: N/A")
            print(f"  24h Change: {bitcoin_data.get('price_change_24h_percent', 'N/A')}%")
        else:
            print(f"✗ Failed to fetch data")
            print(f"  Errors: {result1.get('errors', [])}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 2: Fetch multiple cryptocurrencies
    print("\n" + "-" * 80)
    print("Example 2: Fetch Multiple Cryptocurrencies")
    print("-" * 80)
    
    try:
        result2 = collector.fetch_crypto_prices(
            symbols=["bitcoin", "ethereum", "solana"],
            api_provider="coingecko"
        )
        
        if result2["success"]:
            print(f"✓ Successfully fetched {len(result2['data'])} cryptocurrencies")
            for coin in result2["data"]:
                print(f"  {coin.get('symbol', 'N/A').upper()}: ${coin.get('price_usd', 'N/A')}")
        else:
            print(f"✗ Failed to fetch data")
            print(f"  Errors: {result2.get('errors', [])}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 3: Error handling - invalid symbol
    print("\n" + "-" * 80)
    print("Example 3: Error Handling - Invalid Symbol")
    print("-" * 80)
    
    try:
        result3 = collector.fetch_crypto_prices(
            symbols=["invalid-coin-xyz"],
            api_provider="coingecko",
            retry_count=2
        )
        
        if not result3["success"]:
            print(f"✓ Correctly handled invalid symbol")
            print(f"  Successful fetches: {result3['metadata']['successful_fetches']}")
            print(f"  Failed fetches: {result3['metadata']['failed_fetches']}")
            if result3.get("warnings"):
                print(f"  Warnings: {result3['warnings']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 4: Data validation
    print("\n" + "-" * 80)
    print("Example 4: Data Validation")
    print("-" * 80)
    
    try:
        result4 = collector.fetch_crypto_prices(
            symbols=["bitcoin", "ethereum"],
            api_provider="coingecko"
        )
        
        if result4["success"]:
            validation_result = collector.validate_data(result4["data"])
            report = validation_result["validation_report"]
            
            print(f"✓ Validation completed")
            print(f"  Total records: {report['total_records']}")
            print(f"  Complete records: {report['complete_records']}")
            print(f"  Incomplete records: {report['incomplete_records']}")
            print(f"  Consistency checks passed: {report['consistency_checks_passed']}")
            if report['missing_fields']:
                print(f"  Missing fields: {report['missing_fields'][:3]}...")  # Show first 3
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 5: Combined collection workflow
    print("\n" + "-" * 80)
    print("Example 5: Combined API and Web Scraping (Placeholder)")
    print("-" * 80)
    print("\nNote: Web scraping requires actual URLs that allow scraping.")
    print("Usage:")
    print('  result = collector.collect_crypto_data(')
    print('      symbols=["bitcoin", "ethereum"],')
    print('      fetch_api_data=True,')
    print('      scrape_market_info=True,')
    print('      scrape_urls=["https://example-crypto-news.com/trending"],')
    print('      scrape_selectors={')
    print('          "trending_coins": ".trending-coin-name",')
    print('          "news_headlines": "h2.news-title"')
    print('      },')
    print('      validate_data=True')
    print('  )')
    
    # Example 6: Export to JSON and CSV
    print("\n" + "-" * 80)
    print("Example 6: Export to JSON and CSV (Placeholder)")
    print("-" * 80)
    print("\nUsage:")
    print('  result = collector.fetch_crypto_prices(["bitcoin", "ethereum"])')
    print('  collector.export_to_json(result, "crypto_prices.json")')
    print('  collector.export_to_csv(result, "crypto_prices.csv")')
    
    print("\n" + "=" * 80)
    print("Important Notes:")
    print("=" * 80)
    print("""
1. Always respect API rate limits and terms of service
2. CoinGecko free tier: 10-50 calls/minute (varies)
3. CoinCap free tier: 200 calls/minute
4. Implement appropriate rate limiting to avoid overloading APIs
5. Handle errors gracefully - continue with partial data if needed
6. Validate collected data for consistency and completeness
7. Install optional dependencies for better functionality:
   - pip install requests beautifulsoup4 lxml
8. For production use:
   - Consider caching API responses
   - Implement proper error logging
   - Monitor API usage and rate limits
   - Use authenticated endpoints if available
    """)
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
