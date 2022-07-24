import utils
import streamlit as st

# load and precompute stuff
utils.init_model()

# st app
st.title("CVPR Topic Analysis")

with st.form(key='columns_in_form'):
    c1, c2, c3 = st.columns(3)
    with c1:
        text_input = st.text_input("Enter title or any other text here")
    with c2:
        n_paper = st.number_input("Number of papers to show", 1, 100, 5)
    with c3:
        check_box = st.checkbox('Include Preview URLs')

    rec_paper = st.form_submit_button(label = 'Recommend Papers')

    if rec_paper:
        out = utils.get_relevant_papers(text_input, n_paper)
        # show data
        if check_box:
            out['pdf_link'] = out['pdf_link'].apply(utils.make_clickable, args = ('PDF Link',))
            st.write(out[["author", "title", "year", "abstract", "pdf_link", "citation_count"]].to_html(escape = False), unsafe_allow_html = True)
        else:
            st.dataframe(out[["author", "title", "year", "abstract", "pdf_link", "citation_count"]])

with st.form(key='topics'):
    c1, c2 = st.columns(2)
    with c1:
        option = st.selectbox("Which topics would you like to see?", ("hot", "top", "rising"))
    with c2:
        n = st.number_input("Select number of keywords in each topic", 1, 30, 5)

    show_topics = st.form_submit_button(label = 'Show Topics')

    if show_topics:
        top_count = utils.get_top_by_count(n)
        top_citation = utils.get_top_by_citation(n)
        top_rising = utils.get_top_rising(n)

        if option == "hot":
            st.json(str(top_count))
        elif option == "top":
            st.json(str(top_citation))
        elif option == "rising":
            st.json(str(top_rising))