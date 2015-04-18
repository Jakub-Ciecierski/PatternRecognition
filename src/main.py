import util.console as console
import sys
# CHECK ARGUMENTS
console.parse_argv(sys.argv[1:])

import util.global_variables 
import test_templates as tests

# RUN CONFIGS
console.write_header("Run configuration")
console.print_config()

'''
    Native symbols: synthetic; homogeneous; 
    Foreign symbols: synthetic; homogeneous and non-homogeneous
'''
if util.global_variables.TEST_TYPE == util.global_variables.TestType.SYNTHETIC_HOMO_NATIVE:
    tests.synthetic_homo_native()

if util.global_variables.TEST_TYPE == util.global_variables.TestType.GROUPING_ASSESSMENT:
    tests.grouping_assessment()

if util.global_variables.TEST_TYPE == util.global_variables.TestType.FULL:
    tests.full_test()
    
if util.global_variables.TEST_TYPE == util.global_variables.TestType.REAL_DATA:
    tests.real_data()

if util.global_variables.TEST_TYPE == util.global_variables.TestType.REAL_DATA_STATIC_K:
    tests.real_data_static_k()
    
if util.global_variables.TEST_TYPE == util.global_variables.TestType.SYNTHETIC_PAPER_1:
    tests.synthetic_test_paper_1()
    
if util.global_variables.TEST_TYPE == util.global_variables.TestType.SEMISYNTHETIC_PAPER_1:
    tests.semisynthetic_test_paper_1()
if util.global_variables.TEST_TYPE == util.global_variables.TestType.SYNTHETIC_PAPER_2:
    tests.synthetic_test_paper_2()