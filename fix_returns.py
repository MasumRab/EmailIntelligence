with open("setup/launch.py", "r") as f:
    text = f.read()

text = text.replace("    process_manager.add_process(process)\n\n\ndef start_node_service", "    process_manager.add_process(process)\n    return process\n\n\ndef start_node_service")
text = text.replace("    process_manager.add_process(process)\n\n\ndef start_gradio_ui", "    process_manager.add_process(process)\n    return process\n\n\ndef start_gradio_ui")
text = text.replace("    process_manager.add_process(process)\n\n\ndef handle_setup", "    process_manager.add_process(process)\n    return process\n\n\ndef handle_setup")
text = text.replace("        if proc.stderr:\n            logger.warning(proc.stderr)\n        return True\n    except Exception as e", "        if proc.stderr:\n            logger.warning(proc.stderr)\n        return proc\n    except Exception as e")


with open("setup/launch.py", "w") as f:
    f.write(text)
