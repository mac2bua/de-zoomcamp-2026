WITH payment_type_lookup AS (
    SELECT
        *
    FROM {{ ref('payment_types') }}
),

renamed AS (
    SELECT
        payment_type,
        description AS payment_description
    FROM payment_type_lookup
)

SELECT
    *
FROM renamed