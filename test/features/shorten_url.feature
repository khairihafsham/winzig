Feature: Show ability to deflate and inflate url

    Scenario: URL without .tld handling
        Given I want to shorten "google"
        When I submit the URL
        Then I should see an error

    Scenario: Missing URL handling
        Given I want to shorten " "
        When I submit the URL
        Then I should see an error

    Scenario: Deflate URL
        Given I want to shorten "google.com"
        When I submit the URL
        Then I should see a new short URL

    Scenario: Deflate same URL
        Given I want to shorten "google.com"
        When I submit the URL
        Then I should see the same short URL

    Scenario: Inflate URL
        Given I want to inflate the previous deflated URL
        When I go to the deflated URL
        Then I should be redirected to "google.com"
