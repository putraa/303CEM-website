""" SPENDBOSS WEBSITE - UserInput.py
    This is the main file for validating user inputs across the site.
    Currently we only have one function for account creation.
    Later updates, storing money variables and other input will go through here.
"""


def mk_account(name, email, password, conf_password):
    """ Account making validation
    This will validate the user input variables for making an account.
    if name have more than one word, it will be separated to forename and surname.
    
    :param name: string of name
    :param email: string of email
    :param password: string of password
    :param conf_password: string of confirm_password
    
    IF email dont have @ sign
        :return: False
    ELSE IF password not same with confirm password
        :return: False
    ELSE
        :return: list of first name, surname, email and password
    """
    fname = name
    surname = ""
    if " " in name:
        for letter in range(len(name), 0, -1):
            if name[letter-1] == " ":
                break
            surname += name[letter-1]
        surname = surname[::-1]
        fname = name[:len(surname)-2*len(surname)]
    if not "@" in email:
        return False
    if password != conf_password:
        return False
    return fname, surname, email, password


