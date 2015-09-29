import util.loader as loader
import util.logger as logger
import util.global_variables as global_v

def run():
    if global_v.NATIVE_FILE_PATH == "":
        __deserialize()
    else:
        __serialize()

def __serialize():
    logger.log_header("Serializing")

    nativeElements = loader.load_native_xls()

    loader.serialize_chosen_elements(nativeElements)

def __deserialize():
    logger.log_header("Deserializing")

    nativeElements = loader.deserialize_native()

    for learning_element in nativeElements.learning_set:
        element_str = str(learning_element.characteristicsValues)
        element_str = element_str.strip("[")
        element_str = element_str.rstrip("]")

        logger.log(element_str,
                    filename="training" + "_" + ".txt",
                    styles=[logger.LogStyle.NONE, logger.LogStyle.FILE_ONLY],
                    text_indent="")
