# **Task 2 – Conditional Probability with NumPy Masks**

## **Detailed Student Explanation**

### **Purpose of This Task**

The goal of Task 2 is to demonstrate a correct understanding of **conditional probability** and to implement it **using NumPy boolean masks only**.
The task focuses on:

* Correct event definition
* Proper denominator selection
* Avoiding common mistakes such as confusing ( P(A|B) ) with ( P(B|A) )

---

## **1. Data Preparation**

The dataset was exported from a Supabase database and contains movie information such as:

* Genre
* Runtime
* Average rating

Some movies have missing rating values (e.g. `"null"` or empty strings). Therefore:

* All data was initially loaded as strings
* Valid rating values were converted to `float`
* Invalid or missing values were converted to `NaN`

This ensures numerical correctness while preserving missing information.

---

## **2. Explicit Event Definitions**

Before performing any calculations, all events were **clearly defined** as NumPy boolean masks:

* **Event A**: The movie genre is *Comedy*
* **Event B**: The movie has a high rating (rating ≥ 7)
* **Event C**: The movie is long (runtime > 120 minutes)
* **Event D**: The movie has a missing rating

Each event is represented by a boolean array of the same length as the dataset.

---

## **3. Meaning of Conditional Probability**

Conditional probability answers the question:

> “What is the probability of event A occurring **given that** event B has already occurred?”

It is defined as:
[
P(A|B) = \frac{\text{Number of cases where both A and B occur}}{\text{Number of cases where B occurs}}
]

A key point is that **the denominator is not the total dataset**, but only the cases where the conditioning event occurs.

---

## **4. Reusable Conditional Probability Function**

A reusable function was written to compute conditional probabilities:

* It uses NumPy masks to compute intersections
* It checks whether the conditioning event occurs at all
* If the denominator is zero, it returns `NaN` instead of dividing by zero

Returning `NaN` is statistically correct because a conditional probability is **undefined** when the conditioning event never occurs.

---

## **5. Computed Conditional Probabilities**

At least **five different conditional probabilities** were computed, including:

* ( P(\text{Comedy} \mid \text{High Rating}) )
* ( P(\text{High Rating} \mid \text{Comedy}) )
* ( P(\text{Long Movie} \mid \text{High Rating}) )
* ( P(\text{High Rating} \mid \text{Long Movie}) )
* ( P(\text{Missing Rating} \mid \text{Comedy}) )

The numerical results clearly show that:
[
P(A|B) \neq P(B|A)
]

because the conditioning event (and therefore the denominator) is different.

---

## **6. Incorrect Conditional Probability (Intentional)**

An intentionally incorrect calculation was included where the total number of movies was used as the denominator instead of the conditioning event.

This demonstrates a common mistake:

* Using the full dataset size computes a **joint probability**
* It does **not** represent a conditional probability

The incorrect result was clearly identified and explained.

---

## **7. Explanation of Denominator Choice**

The denominator in a conditional probability must be:

* The number of times the conditioning event occurs

Using the total number of observations ignores the condition and leads to incorrect results.
This distinction is critical and was explicitly demonstrated both in code and in explanation.

---

## **8. Key Takeaways**

This task demonstrates that:

* Conditional probability must restrict the sample space
* Correct denominator selection is essential
* `NaN` correctly represents undefined conditional probabilities
* NumPy boolean masks provide a clean and efficient solution
* Confusing ( P(A|B) ) with ( P(B|A) ) leads to incorrect conclusions

All calculations strictly follow the assignment rules and use NumPy only.



