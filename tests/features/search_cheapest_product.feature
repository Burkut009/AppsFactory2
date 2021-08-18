#As a new Amazon user, I want to search for the cheapest Snickers and Skittles on the page.
#
#Add the cheapest ones to your Basket and check if the basket calculates the result correctly
#
#Check if on Checkout, without an account, the user gets redirected to the registration page.
#


Feature: search cheapest products
  @wip
  Scenario Outline: As a new Amazon user, I want to search for the cheapest Snickers and Skittles on the page
    Given user is on the Amazon home page
    And   user selects English language
    When  user enters "<product name>" in the searchBox
    And   user clicks search icon
    Then  user is on the searched product result page
    When  user clicks Sort by dropDown
    And   user selects Price: Low to High option
    And   user selects the searched product with lowest price
    Then  user is on the searched product detail page
    And   user should see the correct searched product details
    When  user clicks add to basket button
    And   user clicks basket button
    Then  user is on the Shopping Basket page
    And   user should see the searched products
    And   user checks if the basket calculates the result correctly
    When  clicks  checkout button
    Then  the user gets redirected to the registration page

    Examples:
    |product name|
    |Snickers    |
