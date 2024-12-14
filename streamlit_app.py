# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie!! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie.""")

name_on_order = st.text_input("Name of Smoothie", " ")
st.write("The name of your Smoothie will be : ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose upto 5 ingrefient :', 
    my_dataframe,
    max_selections= 5
)

if ingredients_list:
    ingredients_string = ''

    for i in ingredients_list:
        ingredients_string += i + ' '
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    # st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
