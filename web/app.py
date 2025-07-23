import streamlit as st
from plyfile import PlyData, PlyElement
import numpy as np
import os

def reduce_ply(input_file, reduction_factor):
    plydata = PlyData.read(input_file)
    vertex_data = plydata['vertex'].data
    original_vertices = len(vertex_data)
    new_vertex_count = max(int(original_vertices * reduction_factor), 1)
    indices = np.random.choice(original_vertices, new_vertex_count, replace=False)
    indices.sort()
    vertex = vertex_data[indices]
    property_names = vertex_data.dtype.names
    new_elements = [PlyElement.describe(vertex, 'vertex')]
    for element in plydata.elements:
        if element.name != 'vertex':
            new_elements.append(element)
    new_plydata = PlyData(new_elements, text=plydata.text)
    new_plydata.comments = plydata.comments
    output_file = "reduced_" + os.path.basename(input_file)
    new_plydata.write(output_file)
    return output_file

st.title("PLY File Reducer")

uploaded_file = st.file_uploader("Choose a PLY file", type="ply")
reduction_factor = st.slider("Select reduction factor", 0.1, 1.0, 0.5)

if uploaded_file is not None:
    with open("temp.ply", "wb") as f:
        f.write(uploaded_file.getbuffer())
    output_file = reduce_ply("temp.ply", reduction_factor)
    st.success(f"File reduced successfully! Download {output_file}")
    with open(output_file, "rb") as f:
        st.download_button("Download Reduced File", f, file_name=output_file)