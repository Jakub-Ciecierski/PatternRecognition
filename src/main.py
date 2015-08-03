import util.console as console
import sys
# CHECK ARGUMENTS
console.parse_argv(sys.argv[1:])

import util.global_variables 
import test_templates as tests

# SET UP TEST ID
tests.choose_test()

# RUN CONFIGS
console.init_log_dir()
console.write_header("Run configuration")
console.print_config()

'''
    Native symbols: synthetic; homogeneous; 
    Foreign symbols: synthetic; homogeneous and non-homogeneous
'''
if util.global_variables.TEST_TYPE == util.global_variables.TestType.SYNTHETIC_HOMO_NATIVE:
    tests.synthetic_homo_native()

elif util.global_variables.TEST_TYPE == util.global_variables.TestType.GROUPING_ASSESSMENT:
    tests.grouping_assessment()

elif util.global_variables.TEST_TYPE == util.global_variables.TestType.FULL:
    tests.full_test()
    
elif util.global_variables.TEST_TYPE == util.global_variables.TestType.REAL_DATA:
    tests.real_data()

elif util.global_variables.TEST_TYPE == util.global_variables.TestType.REAL_DATA_STATIC_K:
    tests.real_data_static_k()
    
elif util.global_variables.TEST_TYPE == util.global_variables.TestType.SYNTHETIC_PAPER_1:
    tests.synthetic_test_paper_1()
    
elif util.global_variables.TEST_TYPE == util.global_variables.TestType.SEMISYNTHETIC_PAPER_1:
    tests.semisynthetic_test_paper_1()

elif util.global_variables.TEST_TYPE == util.global_variables.TestType.SYNTHETIC_PAPER_2:
    tests.synthetic_test_paper_2()
    
elif util.global_variables.TEST_TYPE == util.global_variables.TestType.SEMISYNTHETIC_PAPER_2:
    tests.semisynthetic_test_paper_2()
    
elif util.global_variables.TEST_TYPE == util.global_variables.TestType.STATIC_K_SEMISYNTHETIC_PAPER_2:
    tests.static_k_semisynthetic_test_paper_2()

elif util.global_variables.TEST_TYPE == util.global_variables.TestType.PAPER_2:
    tests.paper_2()

else:
    print("\nPlease input proper Test ID\n")
