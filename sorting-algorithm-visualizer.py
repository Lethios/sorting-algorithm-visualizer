import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

st.set_page_config(
    layout="wide",
    page_title="Sorting Algorithm Visualizer",
    initial_sidebar_state="collapsed"
)

st.markdown("<h2 style='text-align: center; color:#E6E6FA;'>Sorting Algorithm Visualizer</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    col_algo_select, col_visualize_btn, col_shuffle_btn, col_spacer = st.columns([2, 1.5, 1.5, 3])

    with col_algo_select:
        selected_algo = st.selectbox(
            "Select Algorithm",
            ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort", "Cycle Sort", "3-way Merge Sort", "Counting Sort", "Radix Sort", "Bucket Sort"],
            index=0,
            key="algorithm_selector",
            label_visibility="collapsed"
        )

    with col_visualize_btn:
        visualize_button = st.button(
            f"Visualize {selected_algo}",
            key="visualize_button_main",
            use_container_width=True
        )

    with col_shuffle_btn:
        shuffle_button = st.button(
            "Shuffle Array",
            key="shuffle_button_main",
            use_container_width=True
        )

    st.markdown("---")

    col_size_slider, col_speed_slider = st.columns(2)

    with col_size_slider:
        array_size = st.slider(
            "Array Size",
            min_value=10,
            max_value=200,
            value=50,
            step=5,
            key="array_size_slider"
        )

    with col_speed_slider:
        animation_speed = st.slider(
            "Animation Speed (ms)",
            min_value=1,
            max_value=1000,
            value=100,
            step=10,
            key="animation_speed_slider"
        )

if 'array' not in st.session_state:
    st.session_state.array = np.random.randint(1, 100, array_size).tolist()

if len(st.session_state.array) != array_size:
    st.session_state.array = np.random.randint(1, 100, array_size).tolist()

if shuffle_button:
    st.session_state.array = np.random.randint(1, 100, array_size).tolist()

def create_bar_chart(array, comparing=None, swapping=None, sorted_indices=None, title="Array Visualization"):
    colors = ['#636EFA'] * len(array)    

    if comparing:
        for idx in comparing:
            if 0 <= idx < len(colors):
                colors[idx] = '#FFA15A'
    
    if swapping:
        for idx in swapping:
            if 0 <= idx < len(colors):
                colors[idx] = '#EF553B'
    
    if sorted_indices:
        for idx in sorted_indices:
            if 0 <= idx < len(colors):
                colors[idx] = '#00CC96'
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(range(len(array))),
            y=array,
            marker_color=colors,
            text=array,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Index",
        yaxis_title="Value",
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig

st.markdown("<br>", unsafe_allow_html=True)
chart_placeholder = st.empty()

with chart_placeholder.container():
    fig = create_bar_chart(st.session_state.array, title="Current Array (Size: {len(st.session_state.array)})")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style='display: flex; justify-content: center; gap: 20px; margin-top: 10px;'>
    <span style='color: #636EFA;'>● Default</span>
    <span style='color: #FFA15A;'>● Comparing</span>
    <span style='color: #EF553B;'>● Swapping</span>
    <span style='color: #00CC96;'>● Sorted</span>
</div>
""", unsafe_allow_html=True)

if visualize_button:
    st.info(f"Starting {selected_algo} visualization...")

    if selected_algo == "Bubble Sort":
        array = st.session_state.array.copy()
        
        for i in range(len(array)):

            swapped = False
            for j in range(0, len(array) - i - 1):
                fig = create_bar_chart(
                    array, 
                    comparing=[j, j + 1],
                    sorted_indices=list(range(len(array) - i, len(array))),
                    title="Bubble Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(animation_speed / 1000)
                
                if array[j] > array[j + 1]:
                    fig = create_bar_chart(
                        array,
                        swapping=[j, j + 1],
                        sorted_indices=list(range(len(array) - i, len(array))),
                        title="Bubble Sort in progress..."
                    )
                    chart_placeholder.plotly_chart(fig, use_container_width=True)

                    array[j], array[j + 1] = array[j + 1], array[j]
                    time.sleep(animation_speed / 1000)

        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Bubble Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        st.success(f"{selected_algo} completed!")
        st.session_state.array = array
    
    elif selected_algo == "Selection Sort":
        array = st.session_state.array.copy()

        for i in range(len(array)):
            min_index = i

            for j in range(i + 1, len(array)):
                fig = create_bar_chart(
                    array,
                    comparing=[j, min_index],
                    sorted_indices=list(range(i)),
                    title="Selection Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"selection_compare_{i}_{j}")
                time.sleep(animation_speed / 1000)

                if array[j] < array[min_index]:
                    min_index = j
            
            if min_index != i:
                fig = create_bar_chart(
                    array,
                    swapping=[i, min_index],
                    sorted_indices=list(range(i)),
                    title="Selection Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"selection_swap_{i}")
                time.sleep(animation_speed / 1000)
                
                array[i], array[min_index] = array[min_index], array[i]

        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Selection Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True, key="selection_complete")
        st.success(f"{selected_algo} completed!")

        st.session_state.array = array

    elif selected_algo == "Insertion Sort":
        array = st.session_state.array.copy()
        step_counter = 0
        
        for i in range(1, len(array)):
            key = array[i]
            j = i - 1

            step_counter += 1
            fig = create_bar_chart(
                array,
                comparing=[i],
                sorted_indices=list(range(i)),
                title=f"Insertion Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"insertion_key_{step_counter}")
            time.sleep(animation_speed / 1000)

            while j >= 0 and key < array[j]:

                step_counter += 1
                fig = create_bar_chart(
                    array,
                    comparing=[j, j + 1],
                    sorted_indices=list(range(i)),
                    title=f"Insertion Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"insertion_shift_{step_counter}")
                time.sleep(animation_speed / 1000)
                
                array[j + 1] = array[j]
                j -= 1
            
            array[j + 1] = key

        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Insertion Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True, key="insertion_complete")
        st.success(f"{selected_algo} completed!")
        st.session_state.array = array

    elif selected_algo == "Merge Sort":
        array = st.session_state.array.copy()
        step_counter = [0]
        
        def merge_sort_viz(arr, left_idx=0, right_idx=None):
            if right_idx is None:
                right_idx = len(arr) - 1
                
            if left_idx >= right_idx:
                return
            
            mid = (left_idx + right_idx) // 2

            step_counter[0] += 1
            fig = create_bar_chart(
                array,
                comparing=list(range(left_idx, right_idx + 1)),
                title=f"Merge Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"merge_divide_{step_counter[0]}")
            time.sleep(animation_speed / 1000)
            
            merge_sort_viz(arr, left_idx, mid)
            merge_sort_viz(arr, mid + 1, right_idx)

            left_part = arr[left_idx:mid + 1]
            right_part = arr[mid + 1:right_idx + 1]
            
            i, j, k = 0, 0, left_idx
            
            while i < len(left_part) and j < len(right_part):
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1

                step_counter[0] += 1
                fig = create_bar_chart(
                    array,
                    comparing=[k],
                    title=f"Merge Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"merge_process_{step_counter[0]}")
                time.sleep(animation_speed / 1000)
                k += 1
            
            while i < len(left_part):
                arr[k] = left_part[i]
                i += 1
                k += 1
            
            while j < len(right_part):
                arr[k] = right_part[j]
                j += 1
                k += 1
        
        merge_sort_viz(array)
        
        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Merge Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True, key="merge_complete")
        st.success(f"{selected_algo} completed!")
        st.session_state.array = array

    elif selected_algo == "Quick Sort":
        array = st.session_state.array.copy()
        step_counter = [0]
        
        def quick_sort_viz(arr, start=0, end=None):
            if end is None:
                end = len(arr) - 1
                
            if start >= end:
                return

            pivot = arr[end]

            step_counter[0] += 1
            fig = create_bar_chart(
                array,
                comparing=[end],
                title=f"Quick Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"quick_pivot_{step_counter[0]}")
            time.sleep(animation_speed / 1000)
            
            i = start - 1
            
            for j in range(start, end):
                step_counter[0] += 1
                fig = create_bar_chart(
                    array,
                    comparing=[j, end],
                    title=f"Quick Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"quick_compare_{step_counter[0]}")
                time.sleep(animation_speed / 1000)
                
                if arr[j] < pivot:
                    i += 1

                    step_counter[0] += 1
                    fig = create_bar_chart(
                        array,
                        swapping=[i, j],
                        title=f"Quick Sort in progress..."
                    )
                    chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"quick_swap_{step_counter[0]}")
                    time.sleep(animation_speed / 1000)
                    
                    arr[i], arr[j] = arr[j], arr[i]

            step_counter[0] += 1
            fig = create_bar_chart(
                array,
                swapping=[i + 1, end],
                title=f"Quick Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"quick_place_{step_counter[0]}")
            time.sleep(animation_speed / 1000)
            
            arr[i + 1], arr[end] = arr[end], arr[i + 1]

            quick_sort_viz(arr, start, i)
            quick_sort_viz(arr, i + 2, end)
        
        quick_sort_viz(array)
        
        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Quick Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True, key="quick_complete")
        st.success(f"{selected_algo} completed!")
        st.session_state.array = array

    elif selected_algo == "Heap Sort":
        array = st.session_state.array.copy()
        
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            comparing_nodes = [i]
            if left < n:
                comparing_nodes.append(left)
            if right < n:
                comparing_nodes.append(right)
                
            fig = create_bar_chart(
                array,
                comparing=comparing_nodes,
                title="Heap Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(animation_speed / 1000)
            
            if left < n and arr[left] > arr[largest]:
                largest = left
            
            if right < n and arr[right] > arr[largest]:
                largest = right
            
            if largest != i:
                fig = create_bar_chart(
                    array,
                    swapping=[i, largest],
                    title="Heap Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(animation_speed / 1000)
                
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)
        
        n = len(array)

        fig = create_bar_chart(
            array,
            title="Heap Sort - Building max heap..."
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(animation_speed / 1000)
        
        for i in range(n // 2 - 1, -1, -1):
            heapify(array, n, i)

        fig = create_bar_chart(
            array,
            title="Heap Sort - Max heap built! Root has maximum value"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(animation_speed / 1000)

        for i in range(n - 1, 0, -1):
            fig = create_bar_chart(
                array,
                swapping=[0, i],
                sorted_indices=list(range(i + 1, n)),
                title="Heap Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(animation_speed / 1000)
            
            array[0], array[i] = array[i], array[0]

            heapify(array, i, 0)
        
        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Heap Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        st.success(f"{selected_algo} completed!")
        st.session_state.array = array

    elif selected_algo == "Cycle Sort":
        array = st.session_state.array.copy()
        index = 0

        while index < len(array) - 1:
            item = array[index]
            count = index

            fig = create_bar_chart(
                array,
                comparing=[index],
                title="Cycle Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(animation_speed / 1000)

            for i in range(index + 1, len(array)):
                if array[i] < item:
                    count += 1

            if count == index:
                index += 1
                continue

            while item == array[count]:
                count += 1

            fig = create_bar_chart(
                array,
                swapping=[index, count],
                title="Cycle Sort in progress..."
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(animation_speed / 1000)
            
            array[count], item = item, array[count]

            while count != index:
                count = index
                for i in range(index + 1, len(array)):
                    if array[i] < item:
                        count += 1

                while item == array[count]:
                    count += 1

                fig = create_bar_chart(
                    array,
                    swapping=[count, index],
                    title="Cycle Sort in progress..."
                )
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(animation_speed / 1000)

                array[count], item = item, array[count]

            index += 1

        fig = create_bar_chart(
            array,
            sorted_indices=list(range(len(array))),
            title="Cycle Sort - Complete!"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        st.success(f"{selected_algo} completed!")
        st.session_state.array = array

    else:
        st.warning(f"{selected_algo} implementation coming soon!")
