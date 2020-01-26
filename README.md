#### Goals:

1. Split a document into sections where each section has similar formatting.
2. Produce regex expressions to pull data points out from each section.
3. Create a luigi pipeline to handle the process.

#### Notebooks:

- Combined Methods:
  - [poc_split_text_and_build_regex_expressions.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_split_text_and_build_regex_expressions.ipynb)

- Generate Regex:
  - [poc_hill_climber.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_hill_climber.ipynb)
  - [poc_dynamic_individual.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_dynamic_individual.ipynb)
  - [poc_dynamic_individual_with_static_ending.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_dynamic_individual_with_static_ending.ipynb)
  - [poc_generate_multiple_regex_expressions.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_generate_multiple_regex_expressions.ipynb)

- Split Documents by change in format:
  - [poc_convert_text_to_image.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_convert_text_to_image.ipynb)
  - [poc_split_text_on_changes_in_format.ipynb](https://github.com/dpasse/vegetable_lasagna/tree/master/projects/regex_gp/notebooks/poc_split_text_on_changes_in_format.ipynb)

- Tasks:
  - Split Documents into Sections: python3 split_text_task.py --local-scheduler SplitTextTask --input-directory "./data"

  - Generate Regex Files: python3 generate_regex_task.py --local-scheduler GenerateRegexTask --input-directory "./data"
    - runs SplitTextTask,


