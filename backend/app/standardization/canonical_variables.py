from app.standardization.models import CanonicalVariable


CANONICAL_VARIABLES = [
    CanonicalVariable(
        name="customer_id",
        display_name="Customer ID",
        description="Unique identifier for the borrower or customer.",
        expected_data_type="string",
        example_use_case="Used to join customer-level data across tables."
    ),
    CanonicalVariable(
        name="account_id",
        display_name="Account ID",
        description="Unique identifier for loan, account, or facility.",
        expected_data_type="string",
        example_use_case="Used to create account-level modelling records."
    ),
    CanonicalVariable(
        name="as_on_date",
        display_name="As-on Date / Observation Date",
        description="Date on which the variable values are observed.",
        expected_data_type="date",
        example_use_case="Used as the modelling observation date."
    ),
    CanonicalVariable(
        name="dpd",
        display_name="Days Past Due",
        description="Number of days the account is past due.",
        expected_data_type="integer",
        example_use_case="Used to derive delinquency status and default indicators."
    ),
    CanonicalVariable(
        name="dpd_bucket",
        display_name="DPD Bucket",
        description="Standard delinquency bucket derived from DPD.",
        expected_data_type="string",
        example_use_case="Examples: Current, 1-30, 31-60, 61-90, 90+."
    ),
    CanonicalVariable(
        name="dpd_last_36_months",
        display_name="DPD Last 36 Months",
        description="Historical monthly DPD values for the last 36 months.",
        expected_data_type="array/integer list",
        example_use_case="Used for behavioural scorecard feature engineering."
    ),
    CanonicalVariable(
        name="default_flag",
        display_name="Default Flag",
        description="Indicator showing whether the account has defaulted.",
        expected_data_type="integer/binary",
        example_use_case="Usually 1 for defaulted account, 0 otherwise."
    ),
    CanonicalVariable(
        name="default_date",
        display_name="Default Date",
        description="Date on which the account first met the default definition.",
        expected_data_type="date",
        example_use_case="Used to create PD target variable."
    ),
    CanonicalVariable(
        name="outstanding_balance",
        display_name="Outstanding Balance",
        description="Current outstanding balance at observation date.",
        expected_data_type="decimal",
        example_use_case="Used as exposure or balance-related feature."
    ),
    CanonicalVariable(
        name="target_default_12m",
        display_name="12-Month Default Target",
        description="Indicator showing whether default occurred within 12 months after observation date.",
        expected_data_type="integer/binary",
        example_use_case="Primary target variable for 12-month PD model."
    ),
]


def get_canonical_variables():
    return CANONICAL_VARIABLES