import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Interactive Blog", layout="wide")
# Display Startup Name at the Top
st.markdown(
    "<h1 style='text-align: center; color: orange;'>Pi-Tute</h1><hr>",
    unsafe_allow_html=True
)

# Admin Credentials
ADMIN_USERNAME = "adminSaffuu"
ADMIN_PASSWORD = "348"

# Check admin login status
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Sidebar Admin Login
if not st.session_state["admin_logged_in"]:
    with st.sidebar.form("Admin Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state["admin_logged_in"] = True
                st.sidebar.success("✅ Admin logged in!")
            else:
                st.sidebar.error("❌ Incorrect username or password!")

# Apply custom styling
st.markdown("""
    <style>
        .title {
            color: orange;
            font-size: 40px !important;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Dummy blog data if not initialized
if "blogs" not in st.session_state:
    st.session_state["blogs"] = {
        "Introduction to AI": "Artificial Intelligence (AI) is the simulation of human intelligence in machines...",
        "Getting Started with Python": "Python is an interpreted, high-level and general-purpose programming language..."
    }

# Sidebar for blog selection
st.sidebar.title("📚 Blog Posts")
for blog in st.session_state["blogs"].keys():
    if st.sidebar.button(blog, key=blog):
        st.session_state["selected_blog"] = blog

# Select the blog to display
selected_blog = st.session_state.get("selected_blog", "Introduction to AI")

# Display Blog Content
st.markdown(f"<div class='title'>{selected_blog}</div>", unsafe_allow_html=True)
st.write(f"*Published on: {datetime.today().strftime('%Y-%m-%d')}*")
st.write(st.session_state["blogs"][selected_blog])

# Blog editing section (Only for Admin)
if st.session_state["admin_logged_in"]:
    st.sidebar.subheader("✍️ Create / Edit Blog")

    # Input fields for editing existing blogs
    blog_title = st.sidebar.text_input("Edit Blog Title", value=selected_blog)
    blog_content = st.sidebar.text_area("Edit Blog Content", value=st.session_state["blogs"].get(selected_blog, ""))

    # Save Changes to Blog
    if st.sidebar.button("Save Changes"):
        st.session_state["blogs"][blog_title] = blog_content
        st.session_state["selected_blog"] = blog_title
        st.sidebar.success("✅ Blog updated successfully!")

    # Delete Blog Option
    if blog_title in st.session_state["blogs"]:
        if st.sidebar.button("🗑️ Delete Blog"):
            del st.session_state["blogs"][blog_title]
            st.sidebar.success(f"✅ '{blog_title}' deleted successfully!")
            if st.session_state["blogs"]:
                st.session_state["selected_blog"] = next(iter(st.session_state["blogs"]))  # Select first blog
            else:
                st.session_state["selected_blog"] = ""  # No blogs left
            st.rerun()

    # Separator for adding a new blog
    st.sidebar.markdown("---")
    st.sidebar.subheader("➕ Add a New Blog")

    # Input for new blog
    new_blog_title = st.sidebar.text_input("New Blog Title", placeholder="Enter new blog title")
    new_blog_content = st.sidebar.text_area("New Blog Content", placeholder="Write your new blog content here...")

    # Button to add new blog
    if st.sidebar.button("Add New Blog"):
        if new_blog_title and new_blog_content:
            if new_blog_title not in st.session_state["blogs"]:
                st.session_state["blogs"][new_blog_title] = new_blog_content
                st.session_state["selected_blog"] = new_blog_title
                st.sidebar.success(f"✅ New blog '{new_blog_title}' added successfully!")
                st.rerun()
            else:
                st.sidebar.error("❌ Blog with this title already exists! Choose a different title.")
        else:
            st.sidebar.error("❌ Please enter both title and content for the new blog.")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state["admin_logged_in"] = False
        st.sidebar.success("✅ Logged out successfully!")
        st.rerun()


# Footer
st.markdown("---")
st.markdown("**Made with ❤️ by MD Shafaque**")
