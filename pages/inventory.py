import streamlit as st

from db import (
    get_inventory,
    get_product,
    insert_product,
    update_product,
    delete_product
)

def show_inventory():

    st.title("Inventory Management")

    tab1, tab2 = st.tabs([
        "Product List",
        "Add Product"
    ])

    # ======================================
    # PRODUCT LIST
    # ======================================

    with tab1:

        df = get_inventory()

        st.dataframe(
            df,
            use_container_width=True,
            height=450
        )

        st.divider()

        product_id = st.number_input(
            "Product ID",
            min_value=1,
            step=1
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Load Product"
            ):

                product = get_product(
                    product_id
                )

                if product:

                    st.session_state.product = product

                else:

                    st.error(
                        "Product Not Found"
                    )

        with col2:

            if st.button(
                "Delete Product"
            ):

                delete_product(
                    product_id
                )

                st.success(
                    "Product Deleted"
                )

                st.rerun()

        # ======================================
        # EDIT PRODUCT
        # ======================================

        if "product" in st.session_state:

            p = st.session_state.product

            st.divider()

            st.subheader(
                "Edit Product"
            )

            product_name = st.text_input(
                "Product Name",
                p["product_name"]
            )

            description = st.text_area(
                "Description",
                p["description"] or ""
            )

            sale_price = st.number_input(
                "Sale Price",
                value=float(
                    p["sale_price"] or 0
                )
            )

            stock_qty = st.number_input(
                "Stock Qty",
                value=int(
                    p["stock_qty"] or 0
                )
            )

            minimum_stock = st.number_input(
                "Minimum Stock",
                value=int(
                    p["minimum_stock"] or 5
                )
            )

            if st.button(
                "Update Product"
            ):

                update_product(
                    p["product_id"],
                    product_name,
                    description,
                    sale_price,
                    stock_qty,
                    minimum_stock
                )

                st.success(
                    "Product Updated"
                )

                st.rerun()

    # ======================================
    # ADD PRODUCT
    # ======================================

    with tab2:

        st.subheader(
            "Add New Product"
        )

        category_id = st.number_input(
            "Category ID",
            min_value=1,
            step=1
        )

        brand_id = st.number_input(
            "Brand ID",
            min_value=1,
            step=1
        )

        product_name = st.text_input(
            "Product Name"
        )

        description = st.text_area(
            "Description"
        )

        cost_price = st.number_input(
            "Cost Price",
            min_value=0.0
        )

        sale_price = st.number_input(
            "Sale Price",
            min_value=0.0
        )

        stock_qty = st.number_input(
            "Stock Quantity",
            min_value=0
        )

        minimum_stock = st.number_input(
            "Minimum Stock",
            min_value=1,
            value=5
        )

        if st.button(
            "Add Product"
        ):

            insert_product(
                category_id,
                brand_id,
                product_name,
                description,
                cost_price,
                sale_price,
                stock_qty,
                minimum_stock
            )

            st.success(
                "Product Added Successfully"
            )

            st.rerun()