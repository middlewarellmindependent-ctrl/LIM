# LIM

| Treatment / Validation | Description |
|-----------------------|-------------|
| Operation Filter (Treatment) | Filters model responses by searching for domain-specific keywords to ensure strict domain adherence. |
| Entity Filter (Treatment) | Matches tokens common between user input and model response, prioritizing nouns as entity candidates. |
| Context/Noun Filter (Treatment) | Analyzes the syntactic context of entities to ensure they correspond to valid nouns in the user input. |
| Similarity Filter (Treatment) | Identifies intersections between user input and model response to remove extraneous or hallucinated content. |
| Clean Aux Filter (Treatment) | Removes auxiliary or attribution words (e.g., "is", "are") from responses, especially in update operations. |
| Extract Attribute (Treatment) | Extracts attribute values from the user input based on attribute keys and delimiters such as "and" or commas. |
| Extract Filter (Treatment) | Identifies filtering keywords (Where, With, When) and extracts relevant sections from the input message. |
| Length Test (Validation) | Verifies that the model response is not a single word or an empty string. |
| In-message Test (Validation) | Ensures that the model response appears in the original user input, preventing hallucinations. |
| Key Test (Validation) | Checks that the attribute value is not identical to its key. |
| Addition Mark Test (Validation) | Detects the presence of addition markers indicating multiple attributes. |
| Entity Test (Validation) | Ensures that attribute values do not coincide with identified entities. |
| Attribute Test (Validation) | Prevents attribute values from matching other attribute keys. |
| Pronoun Test (Validation) | Detects pronouns followed by commas in attribute values. |
| Ignoring Test (Validation) | Identifies ignored pronouns or numerical tokens within model responses. |
| Float Test (Validation) | Ensures that floating-point values are correctly interpreted. |
| Character Test (Validation) | Detects noisy or invalid characters such as punctuation, quotation marks, or assignment symbols. |
