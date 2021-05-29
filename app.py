 
import pickle
import streamlit as st
 
# loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(time,EF,serum_creatinine,age,serum_sodium,HBP):   
 
    # Pre-processing user input    
    if HBP == "Yes":
        HBP = 1
    else:
        HBP = 0
 
  
    # Making predictions 
    prediction = classifier.predict( 
        [[time,EF,serum_creatinine,age,serum_sodium,HBP]])
     
    if prediction == 0:
        pred = 'Will Survive'
    else:
        pred = 'Will Die'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Heart Failure Survival Prediction App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    age = st.number_input("What Is Patient's Age?") 
    HBP = st.selectbox('Does Patient Have High Blood Pressure?',("Yes","No"))
    time = st.number_input("How Long Has Patient Had It?") 
    EF = st.number_input("Ejection Fraction In Percentage")
    serum_creatinine = st.number_input("How much creatinine is in the patient's blood?")
    serum_sodium = st.number_input("How much sodium is in the patient's blood?")
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(time,EF,serum_creatinine,age,serum_sodium,HBP) 
        st.success('Patient {}'.format(result))
        
     
if __name__=='__main__': 
    main()