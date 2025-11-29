# Basic Python - One-Liners Collection

## Overview

This directory contains Python one-liner solutions for common programming tasks. These are quick, Pythonic solutions that demonstrate elegant problem-solving techniques.

## Files

### `python_one_liners.py`

A comprehensive collection of **289 Python one-liner problems and solutions** covering common programming tasks with elegant, Pythonic solutions.

**File Structure:**
- **Problems Section** (Lines 1-1630): Clean problem definitions with number, title, description, and function
- **Main Method** (Lines 1632+): All test code organized by problem number, ready to uncomment and test

**Content Categories:**
- Data Structure Operations - Dictionary manipulations, grouping, flattening, merging
- Text Processing - Case conversion, extraction, formatting, parsing
- List Advanced Operations - Rotation, chunking, partitioning, sliding windows
- Data Validation - Credit cards (Luhn), URLs, JSON parsing, date formats
- Temperature & Unit Conversions
- String Operations
- Date & Time Calculations
- Array & List Manipulations
- Mathematical Operations
- Validation & Checking
- Random Generation
- Geometry & Shapes
- Pattern & Formatting
- Boolean & Validation
- And many more...

## Usage

### Running the File

```bash
# From repository root
python app/basic/python_one_liners.py
```

This will display a summary message. To test specific problems, uncomment the test code in the `main()` function.

### Using the One-Liners

Each problem in the file follows a clean structure:

```python
# Problem X: PROBLEM TITLE
# The function_name function description of what it does.
def function_name(params):
    return solution
```

**To use a one-liner:**
1. Browse through the file to find the problem you need (problems are numbered 1-289)
2. Copy the function definition
3. Adapt it to your specific use case
4. Optionally, uncomment the corresponding test code in `main()` to see it in action

### Testing Problems

All test code is centralized in the `main()` function, organized by problem number. To test a specific problem:

1. Open `python_one_liners.py`
2. Navigate to the `main()` function (around line 1632)
3. Find the test section for your problem (e.g., `# Problem 1 Test Code:`)
4. Uncomment the test code
5. Run the file: `python app/basic/python_one_liners.py`

**Example:**
```python
# In main() function, uncomment:
# Problem 1 Test Code:
#   print(celsius_to_fahrenheit(25))
#   Output: 77.0°F (25°C converted to Fahrenheit)
```

---

## Problem Catalog with Solution Links

**Complete catalog of all 289 problems organized by category.**

### Temperature & Unit Conversions (34 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 1 | Convert Celsius To Fahrenheit | [`celsius_to_fahrenheit`](python_one_liners.py#L30) | [Line 30](python_one_liners.py#L30) |
| 3 | Convert Rgb To Hex | [`rgb_to_hex`](python_one_liners.py#L39) | [Line 39](python_one_liners.py#L39) |
| 10 | Generate Random Hex | [`random_hex`](python_one_liners.py#L74) | [Line 74](python_one_liners.py#L74) |
| 28 | Convert Seconds To Hh:Mm:Ss Format | [`seconds_to_hhmmss`](python_one_liners.py#L167) | [Line 167](python_one_liners.py#L167) |
| 37 | Convert String To Number | [`string_to_number`](python_one_liners.py#L215) | [Line 215](python_one_liners.py#L215) |
| 40 | Count Ones In Binary Representation | [`count_ones`](python_one_liners.py#L230) | [Line 230](python_one_liners.py#L230) |
| 47 | Convert Minutes To Seconds | [`mins_to_secs`](python_one_liners.py#L265) | [Line 265](python_one_liners.py#L265) |
| 50 | Convert Dna To Rna | [`dna_to_rna`](python_one_liners.py#L280) | [Line 280](python_one_liners.py#L280) |
| 52 | Convert An Array To A Comma-Separated String | [`array_to_csv`](python_one_liners.py#L291) | [Line 291](python_one_liners.py#L291) |
| 55 | Convert Minutes To Hours And Minutes | [`mins_to_hours_and_mins`](python_one_liners.py#L309) | [Line 309](python_one_liners.py#L309) |
| 59 | Convert Video Length From Minutes To Seconds | [`minutes_to_seconds`](python_one_liners.py#L329) | [Line 329](python_one_liners.py#L329) |
| 62 | Convert Seconds To Minutes And Seconds | [`SecsToMinsAndSecs`](python_one_liners.py#L344) | [Line 344](python_one_liners.py#L344) |
| 72 | Convert Feet To Meters | [`FeetToMeters`](python_one_liners.py#L397) | [Line 397](python_one_liners.py#L397) |
| 79 | Convert Degrees To Radians | [`DegToRad`](python_one_liners.py#L433) | [Line 433](python_one_liners.py#L433) |
| 80 | Binary Letter Converter | [`ConvertBinary`](python_one_liners.py#L438) | [Line 438](python_one_liners.py#L438) |
| 82 | Convert Days To Years, Months, And Days | [`DaysToYearsMonthsDays`](python_one_liners.py#L448) | [Line 448](python_one_liners.py#L448) |
| 84 | Count Decimal Places | [`GetDecimalPlaces`](python_one_liners.py#L461) | [Line 461](python_one_liners.py#L461) |
| 88 | Convert Hours To Minutes | [`HoursToMinutes`](python_one_liners.py#L487) | [Line 487](python_one_liners.py#L487) |
| 94 | Calculate Pi To N Decimal Places | [`my_pi`](python_one_liners.py#L519) | [Line 519](python_one_liners.py#L519) |
| 97 | Hours, Minutes, And Seconds | [`seconds_to_hours_mins_secs`](python_one_liners.py#L534) | [Line 534](python_one_liners.py#L534) |
| 101 | Convert Video Length To Seconds | [`minutes_to_seconds`](python_one_liners.py#L560) | [Line 560](python_one_liners.py#L560) |
| 105 | Convert Binary Number To Decimal | [`binary_to_decimal`](python_one_liners.py#L588) | [Line 588](python_one_liners.py#L588) |
| 138 | Convert Seconds To Days, Hours, Minutes, And Seconds | [`secs_to_days_hours_mins_secs`](python_one_liners.py#L777) | [Line 777](python_one_liners.py#L777) |
| 152 | Hacker Speak Converter | [`convert_to_hacker_speak`](python_one_liners.py#L859) | [Line 859](python_one_liners.py#L859) |
| 158 | Convert Decimal Number To Octal | [`decimal_to_octal`](python_one_liners.py#L891) | [Line 891](python_one_liners.py#L891) |
| 169 | Convert Decimal Number To Hexadecimal | [`decimal_to_hex`](python_one_liners.py#L957) | [Line 957](python_one_liners.py#L957) |
| 181 | Obsolete Sum Converter | [`get_abs_sum`](python_one_liners.py#L1028) | [Line 1028](python_one_liners.py#L1028) |
| 193 | Color (Hexadecimal Format) | [`random_color_hex`](python_one_liners.py#L1096) | [Line 1096](python_one_liners.py#L1096) |
| 203 | Convert Rgb To Hsl (Hue, Saturation, Lightness) | [`rgb_to_hsl`](python_one_liners.py#L1153) | [Line 1153](python_one_liners.py#L1153) |
| 206 | Convert Yen To Usd | [`yen_to_usd`](python_one_liners.py#L1171) | [Line 1171](python_one_liners.py#L1171) |
| 215 | Calculate The Area Of A Regular Hexagon | [`regular_hexagon_area`](python_one_liners.py#L1228) | [Line 1228](python_one_liners.py#L1228) |
| 217 | Bigint Decimal String Formatter | [`format_bigint`](python_one_liners.py#L1238) | [Line 1238](python_one_liners.py#L1238) |
| 240 | Check If A String Is A Valid Isbn (International Standard Book Number) | [`is_valid_isbn`](python_one_liners.py#L1357) | [Line 1357](python_one_liners.py#L1357) |
| 261 | Check If A String Is A Positive Number (No Sign Or Decimal Allowed) | [`is_positive_number`](python_one_liners.py#L1479) | [Line 1479](python_one_liners.py#L1479) |

### String Operations (58 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 7 | Capitalize A String | [`capitalize_string`](python_one_liners.py#L59) | [Line 59](python_one_liners.py#L59) |
| 9 | Find The Frequency Of Character In A String | [`character_frequency`](python_one_liners.py#L69) | [Line 69](python_one_liners.py#L69) |
| 11 | Create Random Strings | [`random_string`](python_one_liners.py#L79) | [Line 79](python_one_liners.py#L79) |
| 16 | Reverse A String | [`reverse`](python_one_liners.py#L104) | [Line 104](python_one_liners.py#L104) |
| 17 | Check If Array Is Empty | [`is_not_empty`](python_one_liners.py#L109) | [Line 109](python_one_liners.py#L109) |
| 19 | Shuffle An Array | [`shuffle_array`](python_one_liners.py#L119) | [Line 119](python_one_liners.py#L119) |
| 20 | Validate Vowel Sandwich | [`is_vowel_sandwich`](python_one_liners.py#L126) | [Line 126](python_one_liners.py#L126) |
| 22 | Get The Length Of A String | [`get_length`](python_one_liners.py#L137) | [Line 137](python_one_liners.py#L137) |
| 39 | Count The Number Of Words In A String | [`count_words`](python_one_liners.py#L225) | [Line 225](python_one_liners.py#L225) |
| 43 | Check If A String Is Empty | [`empty_string`](python_one_liners.py#L245) | [Line 245](python_one_liners.py#L245) |
| 49 | Check If A String Starts With A Specific Character | [`starts_with_char`](python_one_liners.py#L275) | [Line 275](python_one_liners.py#L275) |
| 58 | Truncate A String To A Given Length | [`truncate_string`](python_one_liners.py#L324) | [Line 324](python_one_liners.py#L324) |
| 61 | Check If A String Is A Valid Email Address | [`IsValidEmail`](python_one_liners.py#L339) | [Line 339](python_one_liners.py#L339) |
| 64 | Spell Out A Word | [`Spelling`](python_one_liners.py#L354) | [Line 354](python_one_liners.py#L354) |
| 74 | Check If A String Contains Only Numbers | [`ContainsOnlyNumbers`](python_one_liners.py#L408) | [Line 408](python_one_liners.py#L408) |
| 83 | Check If An Object Is Empty | [`IsEmptyObject`](python_one_liners.py#L456) | [Line 456](python_one_liners.py#L456) |
| 85 | Remove Whitespace From A String | [`RemoveWhitespace`](python_one_liners.py#L469) | [Line 469](python_one_liners.py#L469) |
| 92 | Check If A String Ends With A Specific Substring | [`ends_with_substring`](python_one_liners.py#L509) | [Line 509](python_one_liners.py#L509) |
| 100 | Count The Occurrences Of A Character In A String | [`count_occurrences`](python_one_liners.py#L555) | [Line 555](python_one_liners.py#L555) |
| 102 | Remove Duplicates From A String | [`remove_duplicates_from_string`](python_one_liners.py#L566) | [Line 566](python_one_liners.py#L566) |
| 108 | Capitalize The First Letter Of Each Word In A String | [`capitalize_words`](python_one_liners.py#L604) | [Line 604](python_one_liners.py#L604) |
| 115 | Shuffle The Characters Of A String | [`shuffle_string`](python_one_liners.py#L640) | [Line 640](python_one_liners.py#L640) |
| 120 | Common Prefix In An Array Of Strings | [`longest_common_prefix`](python_one_liners.py#L669) | [Line 669](python_one_liners.py#L669) |
| 121 | Greeting Function With Conditional Message | [`say_hello_bye`](python_one_liners.py#L674) | [Line 674](python_one_liners.py#L674) |
| 122 | Find The First Non-Repeated Character In A String | [`first_non_repeated_char`](python_one_liners.py#L679) | [Line 679](python_one_liners.py#L679) |
| 125 | Check If A String Is An Anagram Of Another String | [`is_anagram`](python_one_liners.py#L700) | [Line 700](python_one_liners.py#L700) |
| 126 | Compact Phone Number Formatter | [`format_phone_number`](python_one_liners.py#L705) | [Line 705](python_one_liners.py#L705) |
| 130 | Remove Vowels From A String | [`remove_vowels`](python_one_liners.py#L732) | [Line 732](python_one_liners.py#L732) |
| 133 | Check If A String Is A Pangram | [`is_pangram`](python_one_liners.py#L748) | [Line 748](python_one_liners.py#L748) |
| 134 | Reverse The Order Of Words In A Sentence | [`reverse_sentence`](python_one_liners.py#L754) | [Line 754](python_one_liners.py#L754) |
| 137 | Count The Letters In A String (Case-Insensitive) | [`count_letters`](python_one_liners.py#L772) | [Line 772](python_one_liners.py#L772) |
| 150 | Find The Length Of The Longest Word In A Sentence | [`longest_word_length`](python_one_liners.py#L848) | [Line 848](python_one_liners.py#L848) |
| 162 | Vowel Dasher | [`dashed`](python_one_liners.py#L915) | [Line 915](python_one_liners.py#L915) |
| 165 | Check If A String Is A Valid Social Security Number (Ssn) | [`is_valid_ssn`](python_one_liners.py#L934) | [Line 934](python_one_liners.py#L934) |
| 168 | Check If A String Is A Valid Ipv4 Address | [`is_valid_ipv4`](python_one_liners.py#L951) | [Line 951](python_one_liners.py#L951) |
| 170 | Check If A String Is A Valid Date (Yyyy-Mm-Dd Format) | [`is_valid_date`](python_one_liners.py#L962) | [Line 962](python_one_liners.py#L962) |
| 172 | Check If A String Is A Valid Password | [`is_valid_password`](python_one_liners.py#L973) | [Line 973](python_one_liners.py#L973) |
| 175 | Roger'S Shooting Score Calculator | [`roger_shots`](python_one_liners.py#L989) | [Line 989](python_one_liners.py#L989) |
| 176 | Middle Character Of String | [`get_middle`](python_one_liners.py#L994) | [Line 994](python_one_liners.py#L994) |
| 183 | Generate A Random Password | [`random_password`](python_one_liners.py#L1039) | [Line 1039](python_one_liners.py#L1039) |
| 187 | Check If A String Is A Valid Us Phone Number | [`is_valid_us_phone_number`](python_one_liners.py#L1065) | [Line 1065](python_one_liners.py#L1065) |
| 200 | Check If A String Is A Valid Ipv6 Address | [`is_valid_ipv6`](python_one_liners.py#L1136) | [Line 1136](python_one_liners.py#L1136) |
| 202 | Check If A String Is A Valid Mac Address | [`is_valid_mac_address`](python_one_liners.py#L1147) | [Line 1147](python_one_liners.py#L1147) |
| 205 | Neutralize Strings Interaction | [`neutralise`](python_one_liners.py#L1166) | [Line 1166](python_one_liners.py#L1166) |
| 213 | Extend Vowels In A Word | [`extend_vowels`](python_one_liners.py#L1216) | [Line 1216](python_one_liners.py#L1216) |
| 214 | Generate A Random Alphanumeric String | [`random_alphanumeric_string`](python_one_liners.py#L1223) | [Line 1223](python_one_liners.py#L1223) |
| 220 | Find The Shortest Word In A String | [`shortest_word`](python_one_liners.py#L1254) | [Line 1254](python_one_liners.py#L1254) |
| 221 | Find The Longest Word Length In A String | [`longest_word_length`](python_one_liners.py#L1259) | [Line 1259](python_one_liners.py#L1259) |
| 238 | Check If A String Is A Valid Url | [`is_valid_url_alt`](python_one_liners.py#L1347) | [Line 1347](python_one_liners.py#L1347) |
| 239 | Check If A String Is A Valid Tax Identification Number (Tin) | [`is_valid_tin`](python_one_liners.py#L1352) | [Line 1352](python_one_liners.py#L1352) |
| 241 | Check If A String Is A Valid Ip Address | [`is_valid_ip_address`](python_one_liners.py#L1362) | [Line 1362](python_one_liners.py#L1362) |
| 242 | Reverse A String (Using Recursion) | [`reverse_string_recursive`](python_one_liners.py#L1372) | [Line 1372](python_one_liners.py#L1372) |
| 249 | Check If A String Is A Palindrome (Ignoring Non-Alphanumeric Characters) | [`is_palindrome_ignoring_non_alphanumeric`](python_one_liners.py#L1407) | [Line 1407](python_one_liners.py#L1407) |
| 254 | Count The Vowels In A String | [`count_vowels`](python_one_liners.py#L1440) | [Line 1440](python_one_liners.py#L1440) |
| 257 | Find The Ascii Value Of A Character | [`get_ascii_value`](python_one_liners.py#L1455) | [Line 1455](python_one_liners.py#L1455) |
| 258 | Check If A String Is An Isogram (No Repeating Characters) | [`is_isogram`](python_one_liners.py#L1460) | [Line 1460](python_one_liners.py#L1460) |
| 259 | Calculate Hamming Distance (Equal Length) | [`hamming_distance`](python_one_liners.py#L1465) | [Line 1465](python_one_liners.py#L1465) |
| 262 | Find The First Non-Repeating Character | [`find_first_non_repeating_character`](python_one_liners.py#L1484) | [Line 1484](python_one_liners.py#L1484) |

### Date & Time Operations (17 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 5 | Check If Date Is Valid | [`is_date_valid`](python_one_liners.py#L49) | [Line 49](python_one_liners.py#L49) |
| 6 | Find The Day Of Year | [`day_of_year`](python_one_liners.py#L54) | [Line 54](python_one_liners.py#L54) |
| 8 | Find The Number Of Days Between Two Days | [`day_diff`](python_one_liners.py#L64) | [Line 64](python_one_liners.py#L64) |
| 26 | Validate Number Within Bounds | [`int_within_bounds`](python_one_liners.py#L157) | [Line 157](python_one_liners.py#L157) |
| 35 | Get The Current Date In Dd/Mm/Yyyy Format | [`get_current_date`](python_one_liners.py#L205) | [Line 205](python_one_liners.py#L205) |
| 41 | Get The Current Year | [`current_year`](python_one_liners.py#L235) | [Line 235](python_one_liners.py#L235) |
| 45 | Calculate Progress Days | [`progress_days`](python_one_liners.py#L255) | [Line 255](python_one_liners.py#L255) |
| 53 | Check If A Year Is A Leap Year | [`is_leap_year`](python_one_liners.py#L296) | [Line 296](python_one_liners.py#L296) |
| 60 | Between Two Dates In Days | [`DateDifferenceInDays`](python_one_liners.py#L334) | [Line 334](python_one_liners.py#L334) |
| 66 | Get The Day Of The Week From A Date | [`GetDayOfWeek`](python_one_liners.py#L364) | [Line 364](python_one_liners.py#L364) |
| 70 | Get The Month Name From A Date | [`GetMonthName`](python_one_liners.py#L387) | [Line 387](python_one_liners.py#L387) |
| 75 | Get The Current Month (0-Based Index) | [`CurrentMonth`](python_one_liners.py#L413) | [Line 413](python_one_liners.py#L413) |
| 76 | Century From Year | [`CenturyFromYear`](python_one_liners.py#L418) | [Line 418](python_one_liners.py#L418) |
| 111 | Validate Zip Code | [`is_valid`](python_one_liners.py#L619) | [Line 619](python_one_liners.py#L619) |
| 146 | Billable Days Bonus Calculator | [`calculate_bonus`](python_one_liners.py#L828) | [Line 828](python_one_liners.py#L828) |
| 210 | Replace Sausages With "Wurst" | [`wurst_is_better`](python_one_liners.py#L1201) | [Line 1201](python_one_liners.py#L1201) |
| 211 | Update Ages After Years | [`after_n_years`](python_one_liners.py#L1206) | [Line 1206](python_one_liners.py#L1206) |

### Array & List Operations (43 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 4 | Transpose Of A Matrix | [`transpose_matrix`](python_one_liners.py#L44) | [Line 44](python_one_liners.py#L44) |
| 21 | Count True Values In Boolean Array | [`count_true`](python_one_liners.py#L131) | [Line 131](python_one_liners.py#L131) |
| 25 | Check If An Array Is Special | [`is_special_array`](python_one_liners.py#L152) | [Line 152](python_one_liners.py#L152) |
| 29 | Get The Last Element Of An Array | [`get_last_element`](python_one_liners.py#L175) | [Line 175](python_one_liners.py#L175) |
| 31 | Check If All Elements In An Array Are The Same | [`test_jackpot`](python_one_liners.py#L185) | [Line 185](python_one_liners.py#L185) |
| 33 | Sum All Numbers In An Array | [`sum_array`](python_one_liners.py#L195) | [Line 195](python_one_liners.py#L195) |
| 34 | Find The Maximum Value In An Array | [`find_max`](python_one_liners.py#L200) | [Line 200](python_one_liners.py#L200) |
| 44 | Sum Of Index Multiplied Elements | [`index_multiplier`](python_one_liners.py#L250) | [Line 250](python_one_liners.py#L250) |
| 48 | Find The Maximum Value In An Array Of Objects | [`find_max_value`](python_one_liners.py#L270) | [Line 270](python_one_liners.py#L270) |
| 54 | Find The Index Of An Element In An Array | [`find_index`](python_one_liners.py#L301) | [Line 301](python_one_liners.py#L301) |
| 56 | Sorted In Ascending Order | [`is_sorted_ascending`](python_one_liners.py#L314) | [Line 314](python_one_liners.py#L314) |
| 57 | Remove A Specific Element From An Array | [`remove_element`](python_one_liners.py#L319) | [Line 319](python_one_liners.py#L319) |
| 78 | Get The Last N Elements Of An Array | [`LastNElements`](python_one_liners.py#L428) | [Line 428](python_one_liners.py#L428) |
| 81 | Find The Intersection Of Two Arrays | [`FindIntersection`](python_one_liners.py#L443) | [Line 443](python_one_liners.py#L443) |
| 86 | Find The Difference Between Two Arrays | [`ArrayDifference`](python_one_liners.py#L474) | [Line 474](python_one_liners.py#L474) |
| 89 | Get The First N Elements Of An Array | [`FirstNElements`](python_one_liners.py#L492) | [Line 492](python_one_liners.py#L492) |
| 91 | Calculate The Standard Deviation Of An Array Of Numbers | [`standard_deviation`](python_one_liners.py#L502) | [Line 502](python_one_liners.py#L502) |
| 93 | Calculate The Sum Of Squares Of An Array | [`sum_of_squares`](python_one_liners.py#L514) | [Line 514](python_one_liners.py#L514) |
| 95 | Generate An Array Of Random Numbers | [`random_array`](python_one_liners.py#L524) | [Line 524](python_one_liners.py#L524) |
| 103 | Find The Mode Of An Array Of Numbers | [`mode`](python_one_liners.py#L571) | [Line 571](python_one_liners.py#L571) |
| 106 | Sorted In Descending Order | [`sorted_descending`](python_one_liners.py#L593) | [Line 593](python_one_liners.py#L593) |
| 107 | Find The Average Of Even Numbers In An Array | [`average_of_even_numbers`](python_one_liners.py#L598) | [Line 598](python_one_liners.py#L598) |
| 109 | Check If An Array Is A Subset Of Another Array | [`is_subset`](python_one_liners.py#L609) | [Line 609](python_one_liners.py#L609) |
| 110 | Maximum Numbers In An Array | [`min_max`](python_one_liners.py#L614) | [Line 614](python_one_liners.py#L614) |
| 112 | Remove Null Values From A List | [`remove_null`](python_one_liners.py#L624) | [Line 624](python_one_liners.py#L624) |
| 114 | Calculate The Sum Of Cubes Of An Array | [`sum_of_cubes`](python_one_liners.py#L635) | [Line 635](python_one_liners.py#L635) |
| 131 | Generate An Array Of Consecutive Numbers | [`consecutive_numbers`](python_one_liners.py#L737) | [Line 737](python_one_liners.py#L737) |
| 136 | Find The Average Of Odd Numbers In An Array | [`average_of_odd_numbers`](python_one_liners.py#L766) | [Line 766](python_one_liners.py#L766) |
| 154 | Calculate The Sum Of Even Numbers In An Array | [`sum_of_even_numbers`](python_one_liners.py#L869) | [Line 869](python_one_liners.py#L869) |
| 166 | Generate An Array Of Random Numbers Within A Range | [`random_array_in_range`](python_one_liners.py#L939) | [Line 939](python_one_liners.py#L939) |
| 196 | Remove Duplicates From Array | [`remove_duplicates`](python_one_liners.py#L1111) | [Line 1111](python_one_liners.py#L1111) |
| 228 | Drop Elements From Array | [`drop`](python_one_liners.py#L1296) | [Line 1296](python_one_liners.py#L1296) |
| 229 | Maximum Total Of Last Five Elements In An Array | [`max_total`](python_one_liners.py#L1301) | [Line 1301](python_one_liners.py#L1301) |
| 234 | Find The Second Largest Number In An Array | [`second_largest`](python_one_liners.py#L1326) | [Line 1326](python_one_liners.py#L1326) |
| 243 | Count The Occurrences Of Each Element In An Array | [`count_occurrences`](python_one_liners.py#L1377) | [Line 1377](python_one_liners.py#L1377) |
| 244 | Check If Two Arrays Are Equal | [`arrays_are_equal`](python_one_liners.py#L1382) | [Line 1382](python_one_liners.py#L1382) |
| 245 | Find The Minimum Value In An Array | [`find_min_value`](python_one_liners.py#L1387) | [Line 1387](python_one_liners.py#L1387) |
| 246 | Flatten An Array Of Nested Arrays | [`flatten_array`](python_one_liners.py#L1392) | [Line 1392](python_one_liners.py#L1392) |
| 247 | Calculate The Average Of Numbers In An Array | [`find_average`](python_one_liners.py#L1397) | [Line 1397](python_one_liners.py#L1397) |
| 248 | Sum The Squares Of Numbers In An Array | [`sum_squares`](python_one_liners.py#L1402) | [Line 1402](python_one_liners.py#L1402) |
| 250 | Find Bob In A List | [`find_bob`](python_one_liners.py#L1413) | [Line 1413](python_one_liners.py#L1413) |
| 253 | Find The Median Of Numbers In An Array | [`find_median`](python_one_liners.py#L1433) | [Line 1433](python_one_liners.py#L1433) |
| 255 | Calculate Vote Difference | [`get_vote_count`](python_one_liners.py#L1445) | [Line 1445](python_one_liners.py#L1445) |

### Mathematical Operations (22 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 14 | Simple Sum | [`addition`](python_one_liners.py#L94) | [Line 94](python_one_liners.py#L94) |
| 32 | Sum Of Numbers Up To A Given Number | [`add_up`](python_one_liners.py#L190) | [Line 190](python_one_liners.py#L190) |
| 36 | Calculate The Power Of A Number | [`power`](python_one_liners.py#L210) | [Line 210](python_one_liners.py#L210) |
| 63 | Generate A Fibonacci Sequence | [`Fibonacci`](python_one_liners.py#L349) | [Line 349](python_one_liners.py#L349) |
| 67 | Check If A Number Is A Power Of Two | [`IsPowerOfTwo`](python_one_liners.py#L370) | [Line 370](python_one_liners.py#L370) |
| 73 | Check If A Number Is A Perfect Square | [`IsPerfectSquare`](python_one_liners.py#L402) | [Line 402](python_one_liners.py#L402) |
| 77 | Check If A Number Is A Prime Number | [`IsPrime`](python_one_liners.py#L423) | [Line 423](python_one_liners.py#L423) |
| 87 | Check If A Number Is A Fibonacci Number | [`IsFibonacci`](python_one_liners.py#L479) | [Line 479](python_one_liners.py#L479) |
| 116 | Find The Nth Fibonacci Number (Recursive) | [`fibonacci`](python_one_liners.py#L647) | [Line 647](python_one_liners.py#L647) |
| 124 | Exponential Of A Number | [`exponential`](python_one_liners.py#L695) | [Line 695](python_one_liners.py#L695) |
| 139 | Check If A Number Is A Prime Factor Of Another Number | [`is_prime_factor`](python_one_liners.py#L786) | [Line 786](python_one_liners.py#L786) |
| 140 | Find The Largest Prime Factor Of A Number | [`largest_prime_factor`](python_one_liners.py#L791) | [Line 791](python_one_liners.py#L791) |
| 141 | Check If A Number Is A Pronic Square | [`is_pronic_square`](python_one_liners.py#L799) | [Line 799](python_one_liners.py#L799) |
| 161 | Find The Sum Of The First N Natural Numbers | [`sum_of_naturals`](python_one_liners.py#L910) | [Line 910](python_one_liners.py#L910) |
| 173 | Find The Nth Fibonacci Number | [`fibonacci_iterative`](python_one_liners.py#L979) | [Line 979](python_one_liners.py#L979) |
| 177 | Calculate The Volume Of A Cube | [`cube_volume`](python_one_liners.py#L1000) | [Line 1000](python_one_liners.py#L1000) |
| 189 | Factor Chain Checker | [`factor_chain`](python_one_liners.py#L1076) | [Line 1076](python_one_liners.py#L1076) |
| 208 | Calculate Iterated Square Root | [`isqrt`](python_one_liners.py#L1183) | [Line 1183](python_one_liners.py#L1183) |
| 216 | Calculate Cube Diagonal From Volume | [`cube_diagonal`](python_one_liners.py#L1233) | [Line 1233](python_one_liners.py#L1233) |
| 222 | Find The Sum Of Proper Divisors Of A Number | [`sum_of_proper_divisors`](python_one_liners.py#L1264) | [Line 1264](python_one_liners.py#L1264) |
| 227 | Check If A Number Is A Perfect Power | [`is_perfect_power`](python_one_liners.py#L1291) | [Line 1291](python_one_liners.py#L1291) |
| 233 | Calculate The Surface Area Of A Cube | [`cube_surface_area`](python_one_liners.py#L1321) | [Line 1321](python_one_liners.py#L1321) |

### Random Generation (4 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 27 | Generate A Random Number Within A Range | [`random_in_range`](python_one_liners.py#L162) | [Line 162](python_one_liners.py#L162) |
| 42 | Generate A Random Number Between 1 And 10 | [`random_1_to_10`](python_one_liners.py#L240) | [Line 240](python_one_liners.py#L240) |
| 68 | Generate Multiplication Table | [`GenerateMultiplicationTable`](python_one_liners.py#L375) | [Line 375](python_one_liners.py#L375) |
| 199 | Generate A Random Uuid | [`random_uuid`](python_one_liners.py#L1130) | [Line 1130](python_one_liners.py#L1130) |

### Pattern & Formatting (4 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 15 | Pyramid Pattern | [`create_pyramid`](python_one_liners.py#L99) | [Line 99](python_one_liners.py#L99) |
| 30 | Jazzify Chords | [`jazzify`](python_one_liners.py#L180) | [Line 180](python_one_liners.py#L180) |
| 160 | American Format | [`is_valid_phone_number`](python_one_liners.py#L905) | [Line 905](python_one_liners.py#L905) |
| 231 | Calculate The Volume Of A Pyramid | [`pyramid_volume`](python_one_liners.py#L1311) | [Line 1311](python_one_liners.py#L1311) |

### Boolean & Validation (27 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 12 | Find The Odd Occurrence | [`find_odd`](python_one_liners.py#L84) | [Line 84](python_one_liners.py#L84) |
| 13 | Check If A Number Is Even Or Odd | [`is_even`](python_one_liners.py#L89) | [Line 89](python_one_liners.py#L89) |
| 38 | Marathon Distance Checker | [`marathon_distance`](python_one_liners.py#L220) | [Line 220](python_one_liners.py#L220) |
| 46 | Check If A Number Is A Multiple Of 5 | [`is_multiple_of_5`](python_one_liners.py#L260) | [Line 260](python_one_liners.py#L260) |
| 51 | Contains A Specific Value | [`contains_value`](python_one_liners.py#L286) | [Line 286](python_one_liners.py#L286) |
| 65 | Contains Only Unique Values | [`HasUniqueValues`](python_one_liners.py#L359) | [Line 359](python_one_liners.py#L359) |
| 90 | Check If A Number Is Odd | [`is_odd`](python_one_liners.py#L497) | [Line 497](python_one_liners.py#L497) |
| 104 | Check For Repdigit | [`is_repdigit`](python_one_liners.py#L583) | [Line 583](python_one_liners.py#L583) |
| 117 | Symmetry Checker | [`is_symmetrical`](python_one_liners.py#L654) | [Line 654](python_one_liners.py#L654) |
| 127 | Check If A Number Is A Neon Number | [`is_neon_number`](python_one_liners.py#L710) | [Line 710](python_one_liners.py#L710) |
| 129 | Check If A Number Is A Disarium Number | [`is_disarium_number`](python_one_liners.py#L725) | [Line 725](python_one_liners.py#L725) |
| 132 | Check If A Number Is A Pronic Number | [`is_pronic_number`](python_one_liners.py#L742) | [Line 742](python_one_liners.py#L742) |
| 145 | Check If A Number Is A Happy Number | [`is_happy_number`](python_one_liners.py#L823) | [Line 823](python_one_liners.py#L823) |
| 149 | Double Letter Checker | [`has_double_letters`](python_one_liners.py#L843) | [Line 843](python_one_liners.py#L843) |
| 167 | Xo Checker | [`xo_checker`](python_one_liners.py#L944) | [Line 944](python_one_liners.py#L944) |
| 174 | Diving Minigame Checker | [`diving_minigame`](python_one_liners.py#L984) | [Line 984](python_one_liners.py#L984) |
| 180 | Check If A Number Is A Vampire Number | [`is_vampire_number`](python_one_liners.py#L1016) | [Line 1016](python_one_liners.py#L1016) |
| 182 | Check If A Number Is A Duck Number | [`is_duck_number`](python_one_liners.py#L1033) | [Line 1033](python_one_liners.py#L1033) |
| 185 | Check If A Number Is A Kaprekar Number | [`is_kaprekar_number`](python_one_liners.py#L1050) | [Line 1050](python_one_liners.py#L1050) |
| 188 | Sastry Number Checker | [`is_sastry`](python_one_liners.py#L1071) | [Line 1071](python_one_liners.py#L1071) |
| 198 | Check If A Number Is A Leyland Number | [`is_leyland_number`](python_one_liners.py#L1121) | [Line 1121](python_one_liners.py#L1121) |
| 204 | Check If A Number Is A Pandigital Number | [`is_pandigital_number`](python_one_liners.py#L1160) | [Line 1160](python_one_liners.py#L1160) |
| 218 | Check If A Number Is A Reversible Number | [`is_reversible_number`](python_one_liners.py#L1244) | [Line 1244](python_one_liners.py#L1244) |
| 223 | Check If A Number Is A Unitary Perfect Number | [`is_unitary_perfect_number`](python_one_liners.py#L1269) | [Line 1269](python_one_liners.py#L1269) |
| 226 | Check If A Number Is A Harshad Smith Number | [`is_harshad_smith_number`](python_one_liners.py#L1286) | [Line 1286](python_one_liners.py#L1286) |
| 232 | Check If A Number Is A Wedderburn-Etherington Number | [`is_wedderburn_etherington_number`](python_one_liners.py#L1316) | [Line 1316](python_one_liners.py#L1316) |
| 236 | Check If A Number Is A Repunit Number | [`is_repunit_number`](python_one_liners.py#L1337) | [Line 1337](python_one_liners.py#L1337) |

### Geometry & Shapes (27 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 23 | Calculate The Area Of A Circle | [`calculate_circle_area`](python_one_liners.py#L142) | [Line 142](python_one_liners.py#L142) |
| 118 | Maximum Triangle Edge Calculator | [`next_edge`](python_one_liners.py#L659) | [Line 659](python_one_liners.py#L659) |
| 119 | Calculate The Perimeter Of A Rectangle | [`rectangle_perimeter`](python_one_liners.py#L664) | [Line 664](python_one_liners.py#L664) |
| 135 | Hypotenuse Of A Right-Angled Triangle | [`calculate_hypotenuse`](python_one_liners.py#L761) | [Line 761](python_one_liners.py#L761) |
| 147 | Calculate The Volume Of A Sphere | [`sphere_volume`](python_one_liners.py#L833) | [Line 833](python_one_liners.py#L833) |
| 153 | Find The Area Of A Rectangle | [`rectangle_area`](python_one_liners.py#L864) | [Line 864](python_one_liners.py#L864) |
| 156 | Calculate The Volume Of A Cylinder | [`cylinder_volume`](python_one_liners.py#L879) | [Line 879](python_one_liners.py#L879) |
| 164 | Calculate The Area Of A Triangle Given The Base And Height | [`triangle_area`](python_one_liners.py#L929) | [Line 929](python_one_liners.py#L929) |
| 179 | Calculate The Perimeter Of A Triangle | [`triangle_perimeter`](python_one_liners.py#L1011) | [Line 1011](python_one_liners.py#L1011) |
| 184 | Calculate The Area Of A Trapezoid | [`trapezoid_area`](python_one_liners.py#L1045) | [Line 1045](python_one_liners.py#L1045) |
| 186 | Calculate The Volume Of A Cone | [`cone_volume`](python_one_liners.py#L1060) | [Line 1060](python_one_liners.py#L1060) |
| 190 | Calculate Boxes In Algebra Sequence | [`box_seq`](python_one_liners.py#L1081) | [Line 1081](python_one_liners.py#L1081) |
| 191 | Calculate The Volume Of A Cuboid | [`cuboid_volume`](python_one_liners.py#L1086) | [Line 1086](python_one_liners.py#L1086) |
| 194 | Calculate The Area Of A Circle Sector | [`circle_sector_area`](python_one_liners.py#L1101) | [Line 1101](python_one_liners.py#L1101) |
| 195 | Calculate The Area Of A Regular Polygon | [`regular_polygon_area`](python_one_liners.py#L1106) | [Line 1106](python_one_liners.py#L1106) |
| 197 | Calculate The Area Of An Ellipse | [`ellipse_area`](python_one_liners.py#L1116) | [Line 1116](python_one_liners.py#L1116) |
| 201 | Calculate The Area Of A Parallelogram | [`parallelogram_area`](python_one_liners.py#L1142) | [Line 1142](python_one_liners.py#L1142) |
| 219 | Circumference Of A Circle | [`circle_circumference`](python_one_liners.py#L1249) | [Line 1249](python_one_liners.py#L1249) |
| 224 | Calculate The Perimeter Of A Regular Polygon | [`regular_polygon_perimeter`](python_one_liners.py#L1276) | [Line 1276](python_one_liners.py#L1276) |
| 225 | Calculate The Area Of An Equilateral Triangle | [`equilateral_triangle_area`](python_one_liners.py#L1281) | [Line 1281](python_one_liners.py#L1281) |
| 230 | Calculate The Area Of A Regular Pentagon | [`regular_pentagon_area`](python_one_liners.py#L1306) | [Line 1306](python_one_liners.py#L1306) |
| 235 | Calculate The Area Of A Regular Octagon | [`regular_octagon_area`](python_one_liners.py#L1332) | [Line 1332](python_one_liners.py#L1332) |
| 237 | Calculate The Volume Of An Ellipsoid | [`ellipsoid_volume`](python_one_liners.py#L1342) | [Line 1342](python_one_liners.py#L1342) |
| 251 | Calculate The Volume Of A Box | [`box_volume`](python_one_liners.py#L1421) | [Line 1421](python_one_liners.py#L1421) |
| 260 | Calculate The Distance Between Two Points In A 2D Plane | [`calculate_distance`](python_one_liners.py#L1472) | [Line 1472](python_one_liners.py#L1472) |
| 263 | Calculate The Area Of A Kite | [`area_of_kite`](python_one_liners.py#L1492) | [Line 1492](python_one_liners.py#L1492) |
| 264 | Calculate The Area Of A Sector | [`sector_area`](python_one_liners.py#L1497) | [Line 1497](python_one_liners.py#L1497) |

### Data Structure Operations (7 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 265 | Convert List To Dictionary With Index As Key | [`list_to_dict`](python_one_liners.py#L1504) | [Line 1504](python_one_liners.py#L1504) |
| 266 | Merge Multiple Dictionaries | [`merge_dicts`](python_one_liners.py#L1509) | [Line 1509](python_one_liners.py#L1509) |
| 267 | Access Nested Dictionary Value Safely | [`safe_nested_get`](python_one_liners.py#L1514) | [Line 1514](python_one_liners.py#L1514) |
| 268 | Flatten Dictionary With Nested Keys | [`flatten_dict`](python_one_liners.py#L1519) | [Line 1519](python_one_liners.py#L1519) |
| 269 | Group List Items By A Key Function | [`group_by`](python_one_liners.py#L1524) | [Line 1524](python_one_liners.py#L1524) |
| 270 | Invert Dictionary (Swap Keys And Values) | [`invert_dict`](python_one_liners.py#L1529) | [Line 1529](python_one_liners.py#L1529) |
| 271 | Filter Dictionary By Value Condition | [`filter_dict_by_value`](python_one_liners.py#L1534) | [Line 1534](python_one_liners.py#L1534) |

### Text Processing (6 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 272 | Convert Camelcase To Snake_Case | [`camel_to_snake`](python_one_liners.py#L1539) | [Line 1539](python_one_liners.py#L1539) |
| 273 | Convert Snake_Case To Camelcase | [`snake_to_camel`](python_one_liners.py#L1544) | [Line 1544](python_one_liners.py#L1544) |
| 274 | Extract All Numbers From String | [`extract_numbers`](python_one_liners.py#L1549) | [Line 1549](python_one_liners.py#L1549) |
| 275 | Extract All Email Addresses From Text | [`extract_emails`](python_one_liners.py#L1554) | [Line 1554](python_one_liners.py#L1554) |
| 276 | Format Number With Thousand Separators | [`format_number`](python_one_liners.py#L1559) | [Line 1559](python_one_liners.py#L1559) |
| 277 | Split String By Multiple Delimiters | [`split_multiple`](python_one_liners.py#L1564) | [Line 1564](python_one_liners.py#L1564) |

### List Advanced Operations (7 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 278 | Rotate List By N Positions | [`rotate_list`](python_one_liners.py#L1569) | [Line 1569](python_one_liners.py#L1569) |
| 279 | Find All Indices Of An Element | [`find_all_indices`](python_one_liners.py#L1574) | [Line 1574](python_one_liners.py#L1574) |
| 280 | Partition List By Condition | [`partition_list`](python_one_liners.py#L1579) | [Line 1579](python_one_liners.py#L1579) |
| 281 | Chunk List Into Groups Of N | [`chunk_list`](python_one_liners.py#L1584) | [Line 1584](python_one_liners.py#L1584) |
| 282 | Interleave Two Lists | [`interleave_lists`](python_one_liners.py#L1589) | [Line 1589](python_one_liners.py#L1589) |
| 283 | Remove Duplicates While Preserving Order | [`remove_duplicates_ordered`](python_one_liners.py#L1594) | [Line 1594](python_one_liners.py#L1594) |
| 284 | Sliding Window Of Size N | [`sliding_window`](python_one_liners.py#L1599) | [Line 1599](python_one_liners.py#L1599) |

### Data Validation (5 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 285 | Validate Credit Card (Luhn Algorithm) | [`validate_credit_card`](python_one_liners.py#L1604) | [Line 1604](python_one_liners.py#L1604) |
| 286 | Parse Date From Multiple Formats | [`parse_date_multiple_formats`](python_one_liners.py#L1610) | [Line 1610](python_one_liners.py#L1610) |
| 287 | Extract Json From String | [`extract_json_from_string`](python_one_liners.py#L1615) | [Line 1615](python_one_liners.py#L1615) |
| 288 | Validate Url Components | [`validate_url`](python_one_liners.py#L1620) | [Line 1620](python_one_liners.py#L1620) |
| 289 | Extract Domain From Url | [`extract_domain`](python_one_liners.py#L1629) | [Line 1629](python_one_liners.py#L1629) |

### Other (28 problems)

| # | Problem | Function | Line Link |
|---|---------|----------|-----------|
| 2 | Swap Two Variables | [`swap_without_temp`](python_one_liners.py#L34) | [Line 34](python_one_liners.py#L34) |
| 18 | Matchstick Count In Steps | [`match_houses`](python_one_liners.py#L114) | [Line 114](python_one_liners.py#L114) |
| 24 | Move Capital Letters To Front | [`cap_to_front`](python_one_liners.py#L147) | [Line 147](python_one_liners.py#L147) |
| 69 | Shhh Whisperer | [`Shhh`](python_one_liners.py#L381) | [Line 381](python_one_liners.py#L381) |
| 71 | Find The Bomb | [`Bomb`](python_one_liners.py#L392) | [Line 392](python_one_liners.py#L392) |
| 96 | Join Path Portions | [`join_path`](python_one_liners.py#L529) | [Line 529](python_one_liners.py#L529) |
| 98 | Simple Calculator | [`calculator`](python_one_liners.py#L543) | [Line 543](python_one_liners.py#L543) |
| 99 | Find Nemo | [`find_nemo`](python_one_liners.py#L548) | [Line 548](python_one_liners.py#L548) |
| 113 | Maurice'S Racing Snails | [`maurice_wins`](python_one_liners.py#L629) | [Line 629](python_one_liners.py#L629) |
| 123 | One-Liner Bitwise Operations In Python | [`bitwise_and`](python_one_liners.py#L684) | [Line 684](python_one_liners.py#L684) |
| 128 | Recursive Right Shift Mimicker | [`shift_to_right`](python_one_liners.py#L720) | [Line 720](python_one_liners.py#L720) |
| 142 | World Landmass Proportion Calculator | [`area_of_country`](python_one_liners.py#L805) | [Line 805](python_one_liners.py#L805) |
| 143 | Loaded Die Detection | [`is_unloaded`](python_one_liners.py#L810) | [Line 810](python_one_liners.py#L810) |
| 144 | Hand Washing Duration Calculator | [`wash_hands`](python_one_liners.py#L815) | [Line 815](python_one_liners.py#L815) |
| 148 | Discounted Price Calculator | [`calculate_final_price`](python_one_liners.py#L838) | [Line 838](python_one_liners.py#L838) |
| 151 | Stolen Items Loss Calculator | [`calculate_losses`](python_one_liners.py#L853) | [Line 853](python_one_liners.py#L853) |
| 155 | Missing Number Finder | [`find_missing_number`](python_one_liners.py#L874) | [Line 874](python_one_liners.py#L874) |
| 157 | Bbq Skewer Analyzer | [`bbq_skewers`](python_one_liners.py#L884) | [Line 884](python_one_liners.py#L884) |
| 159 | Collatz Sequence Analyzer | [`collatz`](python_one_liners.py#L896) | [Line 896](python_one_liners.py#L896) |
| 163 | Number Itself | [`factors`](python_one_liners.py#L920) | [Line 920](python_one_liners.py#L920) |
| 171 | Chinese Zodiac Sign Identifier | [`get_chinese_zodiac_sign`](python_one_liners.py#L967) | [Line 967](python_one_liners.py#L967) |
| 178 | (Visa, Mastercard, Discover, American Express) | [`is_valid_credit_card`](python_one_liners.py#L1005) | [Line 1005](python_one_liners.py#L1005) |
| 192 | Triangular Number Sequence | [`triangular`](python_one_liners.py#L1091) | [Line 1091](python_one_liners.py#L1091) |
| 207 | Calculate War Of Numbers | [`war_of_numbers`](python_one_liners.py#L1176) | [Line 1176](python_one_liners.py#L1176) |
| 209 | Determine Rock, Paper, Scissors Winner | [`rps`](python_one_liners.py#L1191) | [Line 1191](python_one_liners.py#L1191) |
| 212 | Detect Syncopation In Music | [`has_syncopation`](python_one_liners.py#L1211) | [Line 1211](python_one_liners.py#L1211) |
| 252 | Move Zeros To The End | [`move_zeros`](python_one_liners.py#L1426) | [Line 1426](python_one_liners.py#L1426) |
| 256 | Chatroom Status | [`chatroom_status`](python_one_liners.py#L1450) | [Line 1450](python_one_liners.py#L1450) |

---

## Complete Problem List

The file contains **289 problems** total. For the complete list, browse the [`python_one_liners.py`](python_one_liners.py) file directly. Problems are numbered sequentially from 1 to 289.

### Quick Navigation

- **Problems 1-50**: Basic conversions, string operations, arrays
- **Problems 51-100**: Mathematical operations, validations, data structures
- **Problems 101-150**: Advanced string manipulations, date operations
- **Problems 151-200**: Complex algorithms, pattern matching, data transformations
- **Problems 201-264**: Advanced operations, optimizations, edge cases
- **Problems 265-289**: Data structures, text processing, list operations, data validation

---

## Example Problems

Here are some examples of the clean problem format:

```python
# Problem 1: CONVERT CELSIUS TO FAHRENHEIT
# The celsius_to_fahrenheit function converts Celsius to Fahrenheit.
def celsius_to_fahrenheit(celsius): return (celsius * 9/5) + 32

# Problem 3: CONVERT RGB TO HEX
# The rgb_to_hex function combines the red, green, and blue (RGB) values into a single hexadecimal color code.
def rgb_to_hex(r, g, b):
    return f"#{((r << 16) + (g << 8) + b):06X}"

# Problem 9: FIND THE FREQUENCY OF CHARACTER IN A STRING
# The character_frequency function finds the frequency of characters in a String.
def character_frequency(string):
    return {char: string.count(char) for char in set(string)}

# Problem 265: CONVERT LIST TO DICTIONARY WITH INDEX AS KEY
# The list_to_dict function converts a list to a dictionary where the index is the key and the list element is the value.
def list_to_dict(lst: List[Any]) -> Dict[int, Any]:
    return {i: val for i, val in enumerate(lst)}

# Problem 272: CONVERT CAMELCASE TO SNAKE_CASE
# The camel_to_snake function converts a camelCase string to snake_case.
def camel_to_snake(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

# Problem 285: VALIDATE CREDIT CARD (LUHN ALGORITHM)
# The validate_credit_card function validates a credit card number using the Luhn algorithm.
def validate_credit_card(card_number: str) -> bool:
    digits = [int(d) for d in card_number.replace(' ', '')]
    return sum(digits[-1::-2] + [sum(divmod(d * 2, 10)) for d in digits[-2::-2]]) % 10 == 0 if len(digits) > 0 else False
```

**To test these examples**, uncomment the corresponding test code in the `main()` function (starting around line 1632).

## Problem Categories

The 289 problems cover a wide range of topics:

1. **Data Structure Operations** - Dictionary manipulations, grouping, flattening, merging
2. **Text Processing** - Case conversion, extraction, formatting, parsing
3. **List Advanced Operations** - Rotation, chunking, partitioning, sliding windows
4. **Data Validation** - Credit cards (Luhn), URLs, JSON parsing, date formats
5. **String Manipulation** - Reversing, capitalizing, character operations
6. **Mathematical Operations** - Fibonacci, prime numbers, factorials
7. **Date & Time** - Date validation, day calculations, formatting
8. **Array Operations** - Sorting, filtering, transformations
9. **Data Conversions** - Temperature, color codes, units
10. **Validation** - Email, phone numbers, dates, passwords
11. **Random Generation** - Strings, numbers, colors
12. **Geometry** - Area, perimeter, volume calculations
13. **Data Structures** - Matrix operations, dictionary manipulations
14. **Functional Programming** - Map, filter, reduce patterns

## File Organization

The file is organized into two main sections:

1. **Problem Definitions** (Lines 1-1630)
   - Clean, simple format: Problem number, title, description, function
   - Easy to browse and understand
   - No test code cluttering the definitions
   - Later problems (265+) include type hints for better clarity

2. **Test Suite** (Lines 1632+)
   - All test code centralized in `main()` function
   - Organized by problem number
   - Easy to uncomment and test specific problems
   - Each test section includes expected output

## Time Estimates

- **Browsing**: 5-10 minutes to find a specific solution
- **Understanding**: 2-5 minutes per one-liner
- **Testing**: 1-2 minutes to uncomment and run test code
- **Adaptation**: 5-10 minutes to adapt to your use case
- **Total**: 15-20 minutes per problem (as per repository guidelines)

## Source

These problems were migrated from the `Python_One_Liners.docx` reference document on **2025-11-27**.

## Contributing

To add new one-liners:

1. Follow the format with type hints:
   ```python
   # Problem X: PROBLEM TITLE IN UPPERCASE
   # The function_name function description of what it does.
   def function_name(params: Type) -> ReturnType:
       return one_liner_solution
   ```

2. Add corresponding test code in the `main()` function:
   ```python
   # Problem X Test Code:
   # print(function_name(test_params))
   # Output: expected_output
   ```

3. Requirements:
   - Problem number must be sequential (next available number, currently 290)
   - Must be a true one-liner (single return statement)
   - Include type hints for parameters and return type
   - Use descriptive function names (snake_case)
   - Group similar problems together when possible
   - Update the file header with new total count

4. See `/docs/templates/basic_python_template.py` for the complete template format

## Notes

- All code is preserved as-is from the original document
- Problems are clean and easy to read - no inline test code
- Test code is centralized in `main()` function for easy testing
- Use the line links above to jump directly to function definitions
- Focus is on Pythonic, concise solutions
- The file is meant as a reference - adapt the code to your needs

## Related Files

- `/docs/templates/basic_python_template.py` - Template for adding new one-liners
- `/docs/formatting_guide.md` - Code style standards

---

**Happy Coding!** 🚀
