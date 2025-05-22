
skill(root).
skill(creative).
skill(art).
skill(music).
skill(painting).
skill(watercolor).
skill(oil_painting).
skill(digital_art).
skill(guitar).
skill(piano).

% Tree connections
parent(creative, root).

parent(art, creative).
parent(music, creative).

parent(painting, art).
parent(watercolor, painting).
parent(oil_painting, painting).
parent(digital_art, art).

parent(guitar, music).
parent(piano, music).

