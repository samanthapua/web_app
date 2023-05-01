import streamlit as st
import numpy as np
import pandas as pd
import io

footer = """
<style>
footer{
	visibility:hidden;
}
footer:after{
	visibility:visible;
	content:'Developed by Samantha Pua @ 2022';
	display:block;
	position: relative;
	color: white;
	padding: 5px;
	top: 3px;
}
</style>
"""
st.title('Preliminary Data Analysis App')



def main():
	st.markdown(footer,unsafe_allow_html=True)
	activities=['About','Preliminary Data Analysis']
	option = st.sidebar.selectbox('Select options:', activities)

	if option == 'Preliminary Data Analysis':
		st.subheader("Preliminary Data Analysis")
		uploaded_file = st.file_uploader("Upload dataset:", type =['csv','xlsx'])
		
		if uploaded_file:
			if uploaded_file.type =="text/csv":
				df = pd.read_csv(uploaded_file)
				st.success("CSV file ingested successfully. "  + str(df.shape[0]) + " rows loaded.")
				st.write(df.head(20))
				
			
			elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
				df = pd.read_excel(uploaded_file)
				st.success("DXLSX file ingested successfully." + str(df.shape[0]) + " rows loaded.")
				st.write(df.head(20))

			else:
				st.write(uploaded_file.type)
				st.warning('File not ingested', icon="⚠️")

			if st.checkbox("Display top 200 rows"):
				st.write(df.head(200))

			if st.checkbox("Display shape"):
				st.write(df.shape)

			if st.checkbox("Display column names"):
				st.write(df.columns)

			if  st.checkbox("Display summary"):
				st.write(df.describe().T)

			if st.checkbox("Display columns null summary"):
				buffer = io.StringIO()
				df1 = df
				df1.columns = df1.columns.str.replace(' ','_')
				df1.info(buf=buffer)
				s = buffer.getvalue()
				df_info = s.split('\n')
				

				counts = []
				names = []
				nn_count = []
				dtype = []

				for i in range (5, len(df_info)-3):
					line = df_info[i].split()
					counts.append(line[0])
					names.append(line[1])
					nn_count.append(line[2])
					dtype.append(line[4])
				df_info = pd.DataFrame(data = {'Columns':names,'Non-null count': nn_count, 'Total count': df.shape[0],'Data type': dtype})
				df_info['Columns'] = df_info.Columns.replace({'_':' '}, regex=True)
				df_info['Null count'] = df_info.apply(lambda x: int(x['Total count']) - int(x['Non-null count']), axis=1)
				df_info['Null percentage'] = round( df_info['Null count']/df_info['Total count']*100 , 2).astype(str) + '%'
				st.write(df_info.loc[:,['Columns','Null count','Non-null count','Null percentage','Total count','Data type']])


			if st.checkbox("Select multiple columns to view"):
				selected_columns = st.multiselect('Select preferred columns:',df.columns)
				df1 = df[selected_columns]
				st.dataframe(df1)

			if st.checkbox('Display correlation of dataset columns'):
				st.write(df.corr())

			if st.checkbox('Download cleaned data'):
				

				csv = df.to_csv().encode('utf-8')
				st.download_button(label = 'Export as CSV', data = csv, file_name = uploaded_file.name.split('.',1)[0] + '_cleaned.csv', mime = 'text/csv') 
				

	elif option == 'About':
		st.subheader("About App " + " 💻 ")
		st.write("Data scientists and analysts typically spend most of their time doing preliminary analysis on the datasets they are consuming. This app aims to reduce the time spent by automating the long chunky codes they typically do to have a quick overview.")
		
		st.subheader("Functions include:")
		st.markdown("- Insights and purpose that datasets can bring")
		st.markdown("- Quick overview of datasets incl. list of column names, data quality of columns and data storage required")
		st.markdown("- Summary of the gaps in datasets that needs to be addressed")
		st.markdown("- Automated steps to clean dataset. Methodology found below.")


		st.subheader("How-to")
		st.write("Simply go to 'Exploratory Data Analysis' tab and upload the required datasets!")
		st.subheader("Methodology of automated cleaning dataset")


		input_feature = st.text_input('Feedback on other use cases')
		
		if input_feature:
			import csv
			feedbacks= []
			feedbacks.append(input_feature)
			df_feedback = pd.DataFrame(data = {'feedback':feedbacks})
			df_feedback.to_csv('feedback.csv',mode ='a',index=False, header = False)
			st.success("Thank you for your feedback")

			
		st.markdown('''
		<style>
		[data-testid="stMarkdownContainer"] ul{
    	list-style-position: inside;
		}
		</style>
		''', unsafe_allow_html=True)

if __name__ == '__main__':
	main()
