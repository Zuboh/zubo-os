from tools.file_tools  import TOOL_SCHEMAS as FILE_SCHEMAS,   read_file, search_vault, list_files, write_file
from tools.bash_tool   import TOOL_SCHEMAS as BASH_SCHEMAS,   bash
from tools.memory_tool import TOOL_SCHEMAS as MEMORY_SCHEMAS, write_memory, read_memory

TOOL_SCHEMAS = FILE_SCHEMAS + BASH_SCHEMAS + MEMORY_SCHEMAS

TOOL_DISPATCH: dict = {
    "read_file":    read_file,
    "search_vault": search_vault,
    "list_files":   list_files,
    "write_file":   write_file,
    "bash":         bash,
    "write_memory": write_memory,
    "read_memory":  read_memory,
}
