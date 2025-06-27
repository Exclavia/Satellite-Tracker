import os
from skyfield.api import load

# Downloads Keplarian(Keps) Elements from Celestrak, only if file hasn't been download yet
# + only if previous file is more than max_days old (default 7.0)
def get_keps(sat_group:str, file_format:str, max_days=7.0):
    data_dir = "data\\keps"
    s_group = sat_group
    kep_format = file_format
    file_name = f"{s_group}.{kep_format}"
    # Check if data directory exists.
    if os.path.exists(data_dir):
        file_path = os.path.join(data_dir, file_name)
        m_days = max_days
        url_base = "https://celestrak.org/NORAD/elements/gp.php"
        url_opt = f"?GROUP={s_group}&FORMAT={kep_format}"
        url = url_base + url_opt
        if not load.exists(file_path) or load.days_old(file_path) >= m_days:
            load.download(url, filename=file_path)
        return file_path
    else:
        print(f"{data_dir} does not exist.")
        return None