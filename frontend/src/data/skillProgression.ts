/**
 * Skill Progression Map for Python Quest Course
 *
 * Maps each lesson to:
 * - new_concepts: concepts introduced in this lesson
 * - known_before: concepts the student should already know
 * - forbidden_before: concepts that should NOT appear in this lesson's tasks/dialogues
 * - concepts_known_after: all concepts the student knows after completing this lesson
 *
 * Used for:
 * - Course quality audit (pedagogical prerequisite checking)
 * - Adaptive feedback system (what concepts can be referenced)
 * - Content validation (ensure no premature concept usage)
 */

export interface SkillProgressionEntry {
  new_concepts: string[]
  known_before: string[]
  forbidden_before: string[]
  concepts_known_after: string[]
}

export interface SkillProgressionMap {
  meta: {
    description: string
    version: string
  }
  concept_categories: Record<string, string[]>
  lessons: Record<string, SkillProgressionEntry>
  recaps: Record<string, { covers_lessons: string[]; concepts_covered: string[] }>
}

export const SKILL_PROGRESSION: SkillProgressionMap = {
  meta: {
    description: "Skill progression map for Python Quest course",
    version: "1.0",
  },
  concept_categories: {
    io: ["print", "input"],
    types: ["string", "int", "float", "bool", "type_conversion"],
    control_flow: ["if", "else", "elif", "comparison", "logical_ops"],
    data_structures: ["list", "dict", "tuple"],
    loops: ["for", "while", "range", "break", "continue"],
    functions: ["function_def", "function_call", "return"],
    modules: ["import", "random"],
    strings_advanced: ["f_string", "string_methods", "string_formatting"],
    algorithms: ["min_max", "sum", "nested_loops", "accumulator"],
  },
  lessons: {
    "1-1": {
      new_concepts: ["print"],
      known_before: [],
      forbidden_before: ["variables", "input", "if", "else", "for", "while", "int", "comparison", "string_methods", "f_string", "functions", "list", "import"],
      concepts_known_after: ["print"],
    },
    "1-2": {
      new_concepts: ["string", "quotes", "string_literal"],
      known_before: ["print"],
      forbidden_before: ["variables", "input", "if", "else", "int", "comparison"],
      concepts_known_after: ["print", "string"],
    },
    "1-3": {
      new_concepts: ["variables", "assignment", "variable_naming"],
      known_before: ["print", "string"],
      forbidden_before: ["input", "if", "else", "int", "comparison", "for", "while"],
      concepts_known_after: ["print", "string", "variables"],
    },
    "1-4": {
      new_concepts: ["input"],
      known_before: ["print", "string", "variables"],
      forbidden_before: ["if", "else", "int", "comparison", "for", "while", "functions"],
      concepts_known_after: ["print", "string", "variables", "input"],
    },
    "1-5": {
      new_concepts: ["int", "type_conversion", "number"],
      known_before: ["print", "string", "variables", "input"],
      forbidden_before: ["if", "else", "comparison", "for", "while", "functions"],
      concepts_known_after: ["print", "string", "variables", "input", "int"],
    },
    "1-6": {
      new_concepts: ["arithmetic_operator", "expression"],
      known_before: ["print", "string", "variables", "input", "int"],
      forbidden_before: ["if", "else", "comparison", "for", "while", "functions"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator"],
    },
    "1-7": {
      new_concepts: ["comparison", "true_false", "bool"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator"],
      forbidden_before: ["if", "else", "elif", "for", "while", "functions", "list", "logical_ops"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false"],
    },
    "1-8": {
      new_concepts: ["if", "condition"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false"],
      forbidden_before: ["else", "elif", "for", "while", "functions", "logical_ops"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if"],
    },
    "1-9": {
      new_concepts: ["else"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if"],
      forbidden_before: ["elif", "for", "while", "functions", "logical_ops"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else"],
    },
    "2-1": {
      new_concepts: ["float", "number_types", "division"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else"],
      forbidden_before: ["for", "while", "functions", "list", "f_string", "random", "string_methods"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float"],
    },
    "2-2": {
      new_concepts: ["string_methods", "str_methods"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float"],
      forbidden_before: ["for", "while", "functions", "list", "f_string", "random"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods"],
    },
    "2-3": {
      new_concepts: ["f_string", "string_formatting"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods"],
      forbidden_before: ["for", "while", "functions", "list", "random", "elif", "logical_ops"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string"],
    },
    "2-4": {
      new_concepts: ["import", "random", "module"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string"],
      forbidden_before: ["for", "while", "functions", "list", "elif", "logical_ops"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random"],
    },
    "2-5": {
      new_concepts: ["elif"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random"],
      forbidden_before: ["for", "while", "functions", "list", "logical_ops"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random", "elif"],
    },
    "2-6": {
      new_concepts: ["logical_ops", "and", "or", "not"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random", "elif"],
      forbidden_before: ["for", "while", "functions", "list"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random", "elif", "logical_ops"],
    },
    "3-1": {
      new_concepts: ["for", "loop"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random", "elif", "logical_ops"],
      forbidden_before: ["while", "functions", "list", "break", "continue", "nested_loop"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "float", "string_methods", "f_string", "import", "random", "elif", "logical_ops", "for"],
    },
    "3-2": {
      new_concepts: ["range"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for"],
      forbidden_before: ["while", "functions", "list", "break", "continue"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range"],
    },
    "3-3": {
      new_concepts: ["list", "list_creation"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range"],
      forbidden_before: ["while", "functions", "break", "continue", "dict", "list_methods"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list"],
    },
    "3-4": {
      new_concepts: ["list_index", "list_access"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list"],
      forbidden_before: ["while", "functions", "break", "continue", "dict", "list_methods"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index"],
    },
    "3-5": {
      new_concepts: ["list_slice", "list_slicing"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index"],
      forbidden_before: ["while", "functions", "break", "continue", "dict", "list_methods"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "list_slice"],
    },
    "3-6": {
      new_concepts: ["for_list", "loop_over_list"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index"],
      forbidden_before: ["while", "functions", "break", "continue", "dict", "list_methods", "nested_loop"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list"],
    },
    "3-7": {
      new_concepts: ["list_append", "list_add"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append"],
    },
    "3-8": {
      new_concepts: ["list_modify", "list_change"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "list_modify"],
    },
    "3-9": {
      new_concepts: ["accumulator", "loop_accumulate"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "list_modify"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "list_modify", "accumulator"],
    },
    "3-10": {
      new_concepts: ["list_filter", "filter_list"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "accumulator"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "accumulator", "list_filter"],
    },
    "3-11": {
      new_concepts: ["min_max_list"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "accumulator", "list_filter"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "accumulator", "list_filter", "min_max_list"],
    },
    "3-12": {
      new_concepts: ["sum_list", "average_list"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "accumulator"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "accumulator", "sum_list"],
    },
    "3-13": {
      new_concepts: ["list_methods", "pop", "remove", "sort"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "accumulator"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "accumulator", "list_methods"],
    },
    "3-14": {
      new_concepts: ["nested_loop", "loop_in_loop"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "accumulator"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "accumulator", "nested_loop"],
    },
    "3-15": {
      new_concepts: ["enumerate"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "enumerate"],
    },
    "3-16": {
      new_concepts: ["list_comprehension"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append"],
      forbidden_before: ["while", "functions", "break", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "list_append", "list_comprehension"],
    },
    "3-17": {
      new_concepts: ["break"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop"],
      forbidden_before: ["while", "functions", "continue", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "break"],
    },
    "3-18": {
      new_concepts: ["continue"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break"],
      forbidden_before: ["while", "functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break", "continue"],
    },
    "3-19": {
      new_concepts: ["while"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break", "continue"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break", "continue", "while"],
    },
    "3-20": {
      new_concepts: ["while_else"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break", "continue", "while"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break", "continue", "while", "while_else"],
    },
    "3-21": {
      new_concepts: ["input_loop", "loop_with_input"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "input_loop"],
    },
    "3-22": {
      new_concepts: ["in_operator", "not_in"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "in_operator"],
    },
    "3-23": {
      new_concepts: ["two_digit", "digit_extraction"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "in_operator"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "in_operator", "two_digit"],
    },
    "3-24": {
      new_concepts: ["alphabet_loop", "char_loop"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "alphabet_loop"],
    },
    "3-25": {
      new_concepts: ["loop_flag", "sentinel"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while"],
      forbidden_before: ["functions", "dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "loop_flag"],
    },
    "3-26": {
      new_concepts: ["function_def", "def", "function_define"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "break", "continue"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "break", "continue", "while", "function_def", "def"],
    },
    "3-27": {
      new_concepts: ["function_param", "function_argument"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param"],
    },
    "3-28": {
      new_concepts: ["function_return", "return"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
    },
    "3-29": {
      new_concepts: ["multiple_param"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "multiple_param"],
    },
    "3-30": {
      new_concepts: ["function_scope", "local_var", "scope"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "function_scope"],
    },
    "3-31": {
      new_concepts: ["function_recap", "function_practice"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "function_scope"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "function_scope"],
    },
    "3-32": {
      new_concepts: ["string_char_index", "string_index", "char_access"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while"],
      forbidden_before: ["dict", "function_def"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index"],
    },
    "3-33": {
      new_concepts: ["string_len", "len"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index"],
      forbidden_before: ["dict", "function_def"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index", "string_len"],
    },
    "3-34": {
      new_concepts: ["string_iteration", "iterate_string"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index", "string_len"],
      forbidden_before: ["dict", "function_def"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index", "string_len", "string_iteration"],
    },
    "3-35": {
      new_concepts: ["string_split", "join"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index", "string_len", "string_iteration"],
      forbidden_before: ["dict", "function_def"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "string_char_index", "string_len", "string_iteration", "string_split"],
    },
    "3-36": {
      new_concepts: ["return_vs_print"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "return_vs_print"],
    },
    "3-37": {
      new_concepts: ["function_list_param"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "function_list_param"],
    },
    "3-38": {
      new_concepts: ["function_default_param"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "function_default_param"],
    },
    "3-39": {
      new_concepts: ["practical_loop", "loop_applied"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop"],
      forbidden_before: ["dict", "function_def"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "practical_loop"],
    },
    "3-40": {
      new_concepts: ["problem_decomposition"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def", "function_param", "function_return", "problem_decomposition"],
    },
    "3-41": {
      new_concepts: ["all_review"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def", "function_param", "function_return"],
    },
    "4-1": {
      new_concepts: ["nested_while", "while_advanced"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def", "function_param", "function_return", "nested_while"],
    },
    "4-2": {
      new_concepts: ["while_loop_condition"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "while_loop_condition"],
    },
    "4-3": {
      new_concepts: ["number_guessing_game"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "number_guessing_game"],
    },
    "4-4": {
      new_concepts: ["menu_system", "user_menu"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "menu_system"],
    },
    "4-5": {
      new_concepts: ["data_validation", "input_validation"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "data_validation"],
    },
    "4-6": {
      new_concepts: ["combine_loops_conditions"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "combine_loops_conditions"],
    },
    "4-7": {
      new_concepts: ["nested_data", "data_structure"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "nested_data"],
    },
    "4-8": {
      new_concepts: ["matrix", "two_d_list"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "matrix"],
    },
    "4-9": {
      new_concepts: ["search_algorithm", "linear_search"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "search_algorithm"],
    },
    "4-10": {
      new_concepts: ["sort_algorithm", "bubble_sort"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "sort_algorithm"],
    },
    "4-11": {
      new_concepts: ["algo_complexity", "big_o"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "algo_complexity"],
    },
    "4-12": {
      new_concepts: ["recursion"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "recursion"],
    },
    "4-13": {
      new_concepts: ["file_io", "file_read"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "file_io"],
    },
    "4-14": {
      new_concepts: ["file_write"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "file_io"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "file_io", "file_write"],
    },
    "4-15": {
      new_concepts: ["exception_handling", "try_except"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "exception_handling"],
    },
    "4-16": {
      new_concepts: ["while_advanced_practice"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "while_advanced_practice"],
    },
    "4-17": {
      new_concepts: ["nested_loop_practice"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "nested_loop_practice"],
    },
    "4-18": {
      new_concepts: ["list_comprehension_practice"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "list_comprehension"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "list_comprehension", "list_comprehension_practice"],
    },
    "4-19": {
      new_concepts: ["practical_search"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "practical_search"],
    },
    "4-20": {
      new_concepts: ["practical_sort"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "practical_sort"],
    },
    "4-21": {
      new_concepts: ["project_hero_inventory"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "project_hero_inventory"],
    },
    "4-22": {
      new_concepts: ["project_text_adventure"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "project_text_adventure"],
    },
    "4-23": {
      new_concepts: ["mini_project"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "mini_project"],
    },
    "4-24": {
      new_concepts: ["project_dice_game"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "function_def", "project_dice_game"],
    },
    "4-25": {
      new_concepts: ["project_hangman"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "function_def", "project_hangman"],
    },
    "4-26": {
      new_concepts: ["project_quiz_game"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "project_quiz_game"],
    },
    "4-27": {
      new_concepts: ["project_battle_sim"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "random", "function_def", "project_battle_sim"],
    },
    "4-28": {
      new_concepts: ["project_inventory_system"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "project_inventory_system"],
    },
    "4-29": {
      new_concepts: ["project_roguelike"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "random"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "random", "project_roguelike"],
    },
    "4-30": {
      new_concepts: ["project_labyrinth"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "nested_loop", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "function_def", "project_labyrinth"],
    },
    "4-31": {
      new_concepts: ["project_review"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "function_def"],
      forbidden_before: ["dict"],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "nested_loop", "while", "function_def", "project_review"],
    },
    "5-1": {
      new_concepts: ["dict", "dictionary"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict"],
    },
    "5-2": {
      new_concepts: ["module_def", "module_create", "import_own"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict", "module_def"],
    },
    "5-3": {
      new_concepts: ["function_review", "function_mastery"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "function_param", "function_return", "function_review"],
    },
    "5-4": {
      new_concepts: ["final_practice"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict", "final_practice"],
    },
    "5-5": {
      new_concepts: ["project_hero_constructor"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict", "project_hero_constructor"],
    },
    "5-6": {
      new_concepts: ["course_review"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict", "course_review"],
    },
    "5-7": {
      new_concepts: ["final_exam"],
      known_before: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict"],
      forbidden_before: [],
      concepts_known_after: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else", "for", "range", "list", "list_index", "for_list", "while", "function_def", "dict", "final_exam"],
    },
  },
  recaps: {
    "recap-1": {
      covers_lessons: ["1-1", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9"],
      concepts_covered: ["print", "string", "variables", "input", "int", "arithmetic_operator", "comparison", "true_false", "if", "else"],
    },
    "recap-2": {
      covers_lessons: ["2-1", "2-2", "2-3", "2-4", "2-5", "2-6"],
      concepts_covered: ["print", "string", "variables", "input", "int", "float", "arithmetic_operator", "comparison", "true_false", "if", "else", "elif", "string_methods", "f_string", "import", "random", "logical_ops"],
    },
    "recap-3a": {
      covers_lessons: ["3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7", "3-8", "3-9", "3-10", "3-11", "3-12", "3-13", "3-14", "3-15", "3-16", "3-17", "3-18"],
      concepts_covered: ["for", "range", "list", "list_index", "list_slice", "for_list", "list_append", "list_modify", "accumulator", "list_filter", "min_max_list", "sum_list", "list_methods", "nested_loop", "enumerate", "list_comprehension", "break", "continue"],
    },
    "recap-3b": {
      covers_lessons: ["3-19", "3-20", "3-21", "3-22", "3-23", "3-24", "3-25"],
      concepts_covered: ["while", "while_else", "input_loop", "in_operator", "two_digit", "alphabet_loop", "loop_flag"],
    },
    "recap-3c": {
      covers_lessons: ["3-26", "3-27", "3-28", "3-29", "3-30", "3-31", "3-32", "3-33", "3-34", "3-35"],
      concepts_covered: ["function_def", "function_param", "function_return", "multiple_param", "function_scope", "string_char_index", "string_len", "string_iteration", "string_split", "return_vs_print", "function_list_param", "function_default_param"],
    },
    "recap-3d": {
      covers_lessons: ["3-36", "3-37", "3-38", "3-39", "3-40", "3-41"],
      concepts_covered: ["return_vs_print", "function_list_param", "function_default_param", "practical_loop", "problem_decomposition", "all_review"],
    },
    "recap-3": {
      covers_lessons: ["3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7", "3-8", "3-9", "3-10", "3-11", "3-12", "3-13", "3-14", "3-15", "3-16", "3-17", "3-18", "3-19", "3-20", "3-21", "3-22", "3-23", "3-24", "3-25", "3-26", "3-27", "3-28", "3-29", "3-30", "3-31", "3-32", "3-33", "3-34", "3-35", "3-36", "3-37", "3-38", "3-39", "3-40", "3-41"],
      concepts_covered: ["for", "range", "list", "list_index", "list_slice", "for_list", "list_append", "list_modify", "accumulator", "list_filter", "min_max_list", "sum_list", "list_methods", "nested_loop", "enumerate", "list_comprehension", "break", "continue", "while", "while_else", "input_loop", "in_operator", "two_digit", "alphabet_loop", "loop_flag", "function_def", "function_param", "function_return", "multiple_param", "function_scope", "string_char_index", "string_len", "string_iteration", "string_split", "return_vs_print", "function_list_param", "function_default_param", "practical_loop", "problem_decomposition"],
    },
    "recap-4": {
      covers_lessons: ["4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7", "4-8", "4-9", "4-10", "4-11", "4-12", "4-13", "4-14", "4-15", "4-16", "4-17", "4-18", "4-19", "4-20", "4-21", "4-22", "4-23", "4-24", "4-25", "4-26", "4-27", "4-28", "4-29", "4-30", "4-31"],
      concepts_covered: ["for", "range", "list", "nested_loop", "while", "function_def", "function_param", "function_return", "random", "search_algorithm", "sort_algorithm", "recursion", "file_io", "exception_handling", "matrix", "algo_complexity"],
    },
    "recap-5": {
      covers_lessons: ["5-1", "5-2", "5-3", "5-4", "5-5", "5-6", "5-7"],
      concepts_covered: ["dict", "module_def", "function_def", "function_param", "function_return", "for", "range", "list", "while", "if", "else", "print", "input", "int", "string", "variables"],
    },
  },
}

/**
 * Get known concepts for a lesson (inclusive: what the student knows BEFORE this lesson)
 */
export function getKnownBefore(lessonId: string): string[] {
  return SKILL_PROGRESSION.lessons[lessonId]?.known_before ?? []
}

/**
 * Get concepts known after completing a lesson
 */
export function getKnownAfter(lessonId: string): string[] {
  return SKILL_PROGRESSION.lessons[lessonId]?.concepts_known_after ?? []
}

/**
 * Get forbidden concepts for a lesson (concepts that should NOT appear)
 */
export function getForbiddenBefore(lessonId: string): string[] {
  return SKILL_PROGRESSION.lessons[lessonId]?.forbidden_before ?? []
}

/**
 * Get new concepts introduced in a lesson
 */
export function getNewConcepts(lessonId: string): string[] {
  return SKILL_PROGRESSION.lessons[lessonId]?.new_concepts ?? []
}

/**
 * Check if a concept has been taught by this lesson (inclusive)
 */
export function isConceptKnown(lessonId: string, concept: string): boolean {
  const entry = SKILL_PROGRESSION.lessons[lessonId]
  if (!entry) return false
  return entry.concepts_known_after.includes(concept)
}
