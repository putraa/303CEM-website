function validateForm() {
    //retrieve the phone input field value
    var phoneValue = document.getElementById("txtPhone").value;
    var phoneField = document.getElementById("txtPhone");
    var contactForm =  document.getElementById("contact");
    
    if(isNaN(phoneValue))
    {
        phoneField.customError = false;
        phoneField.setCustomValidity('the phone number is in wrong format');
        contactForm.reportValidity();
        return false;
    }
    
}
