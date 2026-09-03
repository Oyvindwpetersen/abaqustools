# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 09:36:00 2025

@author: oyvinpet
"""

#%%

from PIL import Image, ImageDraw, ImageFont
import os
import matplotlib.pyplot as plt
import h5py
import numpy as np

#%%

def stack_images_grid(
    image_files,
    n_rows,
    n_cols,
    cut_top=0,
    cut_bottom=0,
    cut_left=0,
    cut_right=0,
    pad=0,
    bg=(255, 255, 255),
    out_path='stacked_grid.png',
    labels=None,
    label_pos=(5, 5),
    font_path=None,
    font_size=20,
    font_color=(0, 0, 0),
):
    '''
    Stack images into an n_rows x n_cols grid with optional text labels.

    Parameters
    ----------
    labels : list[str] or None
        One label per image (order follows image_files). If None, no text is drawn.
    label_pos : tuple[int,int]
        Position (x,y) for the text relative to top-left corner of each tile.
    font_path : str or None
        Path to .ttf font file. If None, default Pillow font is used.
    font_size : int
        Font size for labels.
    font_color : tuple[int,int,int]
        RGB color of the text.
    '''
    imgs = []
    for fname in image_files:
        if not os.path.exists(fname):
            print(f'[warn] missing file: {fname} (skipping)')
            continue
        try:
            im = Image.open(fname)
            w, h = im.size
            if cut_left + cut_right >= w or cut_top + cut_bottom >= h:
                raise ValueError(f'cropping removes entire image for {fname}')
            box = (cut_left, cut_top, w - cut_right, h - cut_bottom)
            im_c = im.crop(box).convert('RGB')
            imgs.append(im_c)
        except Exception as e:
            print(f'[warn] failed processing {fname}: {e}')

    if not imgs:
        raise RuntimeError('no images loaded')

    min_w = min(im.width for im in imgs)
    min_h = min(im.height for im in imgs)
    norm_imgs = [im.resize((min_w, min_h), Image.LANCZOS) for im in imgs]

    grid_cap = n_rows * n_cols
    tiles = norm_imgs[:grid_cap]
    if len(tiles) < grid_cap:
        blanks = grid_cap - len(tiles)
        for _ in range(blanks):
            tiles.append(Image.new('RGB', (min_w, min_h), bg))



    # prepare font
    if font_path:
        dummy=1
    else:
        font_path = 'C:/Windows/Fonts/arial.ttf'

    font = ImageFont.truetype(font_path, font_size)

    # add labels to tiles
    if labels:
        for i, (tile, lbl) in enumerate(zip(tiles, labels)):
            d = ImageDraw.Draw(tile)
            d.text(label_pos, str(lbl), fill=font_color, font=font)

    canvas_w = n_cols * min_w + pad * (n_cols - 1)
    canvas_h = n_rows * min_h + pad * (n_rows - 1)
    canvas = Image.new('RGB', (canvas_w, canvas_h), bg)

    k = 0
    for r in range(n_rows):
        for c in range(n_cols):
            x = c * (min_w + pad)
            y = r * (min_h + pad)
            canvas.paste(tiles[k], (x, y))
            k += 1

    canvas.save(out_path)
    print(f'[ok] wrote {out_path} ({canvas_w}x{canvas_h}) with {len(imgs)} source images')
    
    
    # Add inside stack_images_grid(), right after `canvas.save(out_path)` and before `return out_path`:
    
    plt.figure()
    plt.imshow(canvas)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


    return out_path


#%%


def import_h5_modal(h5_name):

    hf = h5py.File(h5_name, 'r')
    
    # f
    f = np.array(hf.get('f'))
    
    # Generalized mass
    gm = np.array(hf.get('gm'))
    
    # Node coordinates all nodes (size [N_nodes,4])
    nodecoord = np.array(hf.get('nodecoord'))
    
    # Mode shape matrix for all DOFs (size [6*N_nodes,N_modes])
    phi = np.array(hf.get('phi'))
    
    # Labels corresponding to each row of phi (each DOF), as a list of strings
    phi_label_temp = np.array(hf.get('phi_label'))
    phi_label=phi_label_temp[:].astype('U10').ravel().tolist()
    
    # Mode shape matrix for all DOFs (size [6*N_nodes,N_modes])
    phi_sf = np.array(hf.get('phi_sf'))
    
    # Labels corresponding to each row of phi (each DOF), as a list of strings
    phi_sf_label_temp = np.array(hf.get('phi_sf_label'))
    phi_sf_label=phi_sf_label_temp[:].astype('U10').ravel().tolist()
    
    # f
    elconn = np.array(hf.get('elconn'))
        
    hf.close()
    
    mod=dict()
    
    mod['f']=f
    mod['gm']=gm
    mod['nodecoord']=nodecoord
    mod['phi']=phi
    mod['phi_label']=phi_label
    mod['phi_sf']=phi_sf
    mod['phi_sf_label']=phi_sf_label    
    mod['elconn']=elconn
    
    return mod