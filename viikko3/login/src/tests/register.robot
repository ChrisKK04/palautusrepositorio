*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  tiina
    Set Password  tiina123
    Set Password Confirmation  tiina123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ti
    Set Password  tiina123
    Set Password Confirmation  tiina123
    Click Button  Register
    Register Should Fail With Message  Username is too short

Register With Valid Username And Too Short Password
    Set Username  tiina
    Set Password  ti12
    Set Password Confirmation  ti12
    Click Button  Register
    Register Should Fail With Message  Password is too short

Register With Valid Username And Invalid Password
    Set Username  tiina
    Set Password  tiinatiina
    Set Password Confirmation  tiinatiina
    Click Button  Register
    Register Should Fail With Message  Password doesn't contain symbols outside of letters

Register With Nonmatching Password And Password Confirmation
    Set Username  tiina
    Set Password  tiina123
    Set Password Confirmation  tiina123456
    Click Button  Register
    Register Should Fail With Message  Password and password confirmation don't match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}


*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page