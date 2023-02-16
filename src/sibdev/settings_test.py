# here should be your test settings
from .settings import *

TEST_FILES = {
    "deals_csv": os.path.join(BASE_DIR, "test_files", "deals.csv"),
    "deals_csv_second": os.path.join(BASE_DIR, "test_files", "deals_second.csv"),
    "deals_csv_invalid_file_extension": os.path.join(
        BASE_DIR, "test_files", "invalid_data.csv"
    ),
    "deals_txt_invalid_data": os.path.join(
        BASE_DIR, "test_files", "invalid_extension.txt"
    ),
}
