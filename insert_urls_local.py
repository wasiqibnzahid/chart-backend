import openpyxl
import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tv_charts.settings')

# Setup Django
django.setup()

from server.models import LocalSite  # Adjust the import according to your app structure

def import_local_sites(file_path):
    # Load the workbook and select the active worksheet
    wb = openpyxl.load_workbook(file_path)
    ws = wb['Locales Normal']  # Adjust to your sheet name

    # Initialize variables
    current_site = None
    main_content_type = None
    video_urls = []
    note_urls = []

    for row in ws.iter_rows(min_row=2, values_only=True):  # Adjust min_row based on your file
        if len(row) < 3:
            continue  # Skip rows that don't have enough data

        site_name, content_type, url = row[:3]  # Get only the first three values

        # If we encounter a new site name, save the previous site data
        if site_name and site_name != current_site:
            if current_site:
                save_local_site(current_site, video_urls, note_urls)
            current_site = site_name
            video_urls = []
            note_urls = []

        if content_type:
            main_content_type = content_type

        if main_content_type == 'Video' and url:
            video_urls.append(url)
        elif main_content_type == 'Nota' and url:
            note_urls.append(url)

    # Save the last site data
    if current_site:
        save_local_site(current_site, video_urls, note_urls)

    print('Data imported successfully!')

def save_local_site(name, video_urls, note_urls):
    local_site = LocalSite(
        name=name,
        video_urls=video_urls if video_urls else None,
        note_urls=note_urls if note_urls else None
    )
    local_site.save()

if __name__ == '__main__':
    import_local_sites('local_lighthouse.xlsx')  # Replace with your actual file path
