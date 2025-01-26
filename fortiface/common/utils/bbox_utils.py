def extend_bbox(box, shape_image, ext_w=10, ext_h=10):
    h, w, _ = shape_image
    x1_ext = max(0, box[0] - ext_w)
    y1_ext = max(0, box[1] - ext_h)
    x2_ext = min(w, box[2] + ext_w)
    y2_ext = min(h, box[3] + ext_h)
    return [x1_ext, y1_ext, x2_ext, y2_ext]


def extend_bbox_percent(box, shape_image, ext_w=0.5, ext_h=0.5):
    h, w, _ = shape_image
    w_box = box[2] - box[0]
    h_box = box[3] - box[1]
    x1_ext = max(0, box[0] - int(w_box * ext_w))
    y1_ext = max(0, box[1] - int(h_box * ext_h))
    x2_ext = min(w, box[2] + int(w_box * ext_w))
    y2_ext = min(h, box[3] + int(h_box * ext_h))
    return [x1_ext, y1_ext, x2_ext, y2_ext]
