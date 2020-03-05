Feature: Playout an asset
  In order to use an asset for tests
  As a dev
  I want to check the playability of an asset with playable tool

  Scenario: Play by title
    Given I playout "The Firm"
    Then exit status is OK

  Scenario: Play by title on integration environment
    Given I playout "-v 1 --env integration The Firm"
    Then output contains "playout.integration.nowtv.bskyb.com"

  Scenario: Play by crid
    Given I playout "458431384f556510VgnVCM1000000b43150a____"
    Then exit status is OK

  Scenario: Play unknown title - fails
    Given I playout "unknown"
    Then exit status is "1"

  Scenario: List available crids
    Given I list all available QA crids
    Then output contains "The Firm"



