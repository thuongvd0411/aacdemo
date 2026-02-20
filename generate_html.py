import os
import urllib.parse

html_header = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AAC Thẻ Hình Ảnh / AAC Images Gallery</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #0f172a;
            --surface-color: rgba(30, 41, 59, 0.7);
            --text-color: #f8fafc;
            --text-muted: #94a3b8;
            --card-bg: rgba(255, 255, 255, 0.05);
            --border-color: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-color);
            color: var(--text-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(79, 70, 229, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(236, 72, 153, 0.15) 0%, transparent 50%);
            background-attachment: fixed;
            min-height: 100vh;
            line-height: 1.6;
        }

        header {
            padding: 3rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(15, 23, 42, 0) 100%);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto 2rem;
        }

        .tabs {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        .tab-btn {
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 0.6rem 1.2rem;
            border-radius: 9999px;
            cursor: pointer;
            font-family: inherit;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(12px);
        }

        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }

        .tab-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.39);
        }

        main {
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1.5rem;
            opacity: 1;
            transition: opacity 0.4s ease;
        }

        .gallery.fading {
            opacity: 0;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            cursor: pointer;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
            z-index: 1;
            pointer-events: none;
        }

        .card:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: rgba(255,255,255,0.3);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }

        .img-container {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 1rem;
            background: rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 2;
        }

        .img-container img {
            width: 90%;
            height: 90%;
            object-fit: contain;
            transition: transform 0.5s ease;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.3));
        }

        .card:hover .img-container img {
            transform: scale(1.1) rotate(2deg);
        }

        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            text-align: center;
            text-transform: capitalize;
            color: #e2e8f0;
            z-index: 2;
            padding: 0 0.5rem;
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        /* Lightbox modal */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            backdrop-filter: blur(5px);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .modal.active {
            display: flex;
            opacity: 1;
        }
        
        .modal img {
            max-width: 90%;
            max-height: 80vh;
            border-radius: 12px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
            margin-bottom: 2rem;
            transform: scale(0.9);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .modal.active img {
            transform: scale(1);
        }
        
        .modal-title {
            font-size: 2rem;
            font-weight: 800;
            color: white;
            text-transform: capitalize;
        }
        
        .close-btn {
            position: absolute;
            top: 2rem;
            right: 2rem;
            background: rgba(255,255,255,0.1);
            border: none;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .close-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: scale(1.1) rotate(90deg);
        }

        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            .gallery { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }
            .card { padding: 0.75rem; }
            .card-title { font-size: 0.95rem; }
        }
    </style>
</head>
<body>
"""

html_footer = """
    <div class="modal" id="imageModal">
        <button class="close-btn" id="closeModal">&times;</button>
        <img id="modalImg" src="" alt="View">
        <div class="modal-title" id="modalTitle"></div>
    </div>

    <script>
        const tabBtns = document.querySelectorAll('.tab-btn');
        const galleryItems = document.querySelectorAll('.card');
        const gallery = document.getElementById('gallery');
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImg');
        const modalTitle = document.getElementById('modalTitle');
        const closeModal = document.getElementById('closeModal');

        // Filtering Logic
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all
                tabBtns.forEach(b => b.classList.remove('active'));
                // Add active class to clicked
                btn.classList.add('active');

                const filter = btn.getAttribute('data-filter');

                // Add fading out effect
                gallery.classList.add('fading');

                setTimeout(() => {
                    galleryItems.forEach(item => {
                        if (filter === 'all' || item.getAttribute('data-category') === filter) {
                            item.style.display = 'flex';
                        } else {
                            item.style.display = 'none';
                        }
                    });
                    
                    // Fade back in
                    gallery.classList.remove('fading');
                }, 300);
            });
        });
        
        // Modal Logic
        galleryItems.forEach(item => {
            item.addEventListener('click', () => {
                const imgSrc = item.getAttribute('data-src');
                const title = item.getAttribute('data-title');
                
                modalImg.src = imgSrc;
                modalTitle.textContent = title;
                modal.classList.add('active');
                document.body.style.overflow = 'hidden'; // prevent scrolling
            });
        });
        
        closeModal.addEventListener('click', () => {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto'; // allow scrolling
        });
        
        modal.addEventListener('click', (e) => {
            if(e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
        
        // Keyboard support for modal
        document.addEventListener('keydown', (e) => {
            if(e.key === 'Escape' && modal.classList.contains('active')) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    </script>
</body>
</html>
"""

def main():
    base_dir = "."
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d[0].isdigit()]
    dirs.sort()

    content_html = ""
    tabs_html = """
    <header>
        <h1>Hình ảnh giao tiếp (AAC)</h1>
        <p class="subtitle">Bộ sưu tập hình ảnh AAC hỗ trợ giao tiếp cho trẻ, được phân loại theo danh mục.</p>
        <div class="tabs">
            <button class="tab-btn active" data-filter="all">Tất cả</button>
    """

    FOLDER_MAPPING = {
        "1_nhu_cau_sinh_hoat": "1 Nhu cầu sinh hoạt",
        "2_hanh_dong": "2 Hành động",
        "3_nguoi_quen_thuoc": "3 Người quen thuộc",
        "4_do_vat_do_choi": "4 Đồ vật Đồ chơi",
        "5_cam_xuc": "5 Cảm xúc",
        "6_tu_chuc_nang": "6 Từ chức năng",
    }

    for d in dirs:
        display_d = FOLDER_MAPPING.get(d, d)
        tabs_html += f'            <button class="tab-btn" data-filter="{d}">{display_d}</button>\n'
    
    tabs_html += """
        </div>
    </header>
    <main>
        <div class="gallery" id="gallery">
    """

    content_html += tabs_html

    for d in dirs:
        folder_path = os.path.join(base_dir, d)
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
        files.sort()

        for f in files:
            file_path = f"{d}/{f}"
            url_path = urllib.parse.quote(file_path)
            # Remove extension and numbers/underscores from name for display
            clean_name = os.path.splitext(f)[0]
            if clean_name[:3].isdigit() and clean_name[3] == '_':
                clean_name = clean_name[4:]
            display_name = clean_name.replace('_', ' ').strip()
            
            card = f"""
            <div class="card" data-category="{d}" data-src="{url_path}" data-title="{display_name}">
                <div class="img-container">
                    <img src="{url_path}" alt="{display_name}" loading="lazy">
                </div>
                <div class="card-title">{display_name}</div>
            </div>
            """
            content_html += card

    content_html += """
        </div>
    </main>
    """

    final_html = html_header + content_html + html_footer

    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_html)

    print("Successfully generated index.html")

if __name__ == "__main__":
    main()
