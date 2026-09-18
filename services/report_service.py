from ml.predict import predict_risk


class ReportService:

    @staticmethod
    def generate(
        project,
        risk,
        recommendation,
        market
    ):

        # =====================================================
        # MACHINE LEARNING PREDICTION
        # =====================================================

        try:

            ml_prediction = predict_risk(
                domain=project.domain,
                budget=project.budget,
                team_size=project.team_size,
                timeline=project.timeline,
                priority="Medium"
            )

        except Exception:

            # Safe fallback if the ML prediction cannot
            # be generated for the supplied project data.

            ml_prediction = risk["level"]


        # =====================================================
        # SUCCESS PROBABILITY
        # =====================================================

        success_probability = int(
            recommendation["success_probability"]
        )


        # =====================================================
        # OVERALL RATING
        # =====================================================

        if success_probability >= 85:

            rating = "★★★★★"
            verdict = "Excellent Project Potential"

        elif success_probability >= 70:

            rating = "★★★★☆"
            verdict = "Very Good Project Potential"

        elif success_probability >= 55:

            rating = "★★★☆☆"
            verdict = "Good Project Potential"

        elif success_probability >= 40:

            rating = "★★☆☆☆"
            verdict = "Moderate Project Potential"

        else:

            rating = "★☆☆☆☆"
            verdict = "High Risk Project"


        # =====================================================
        # EXECUTIVE SUMMARY
        # =====================================================

        summary = (

            f"The project belongs to the "
            f"{market['industry']} industry. "

            f"It currently has a "
            f"{recommendation['health'].lower()} health status "
            f"with a success probability of "
            f"{success_probability}%. "

            f"The rule-based risk assessment reports a "
            f"{risk['level'].strip().lower()} risk level "
            f"with a score of {risk['score']} out of 100. "

            f"The machine-learning model predicts "
            f"{ml_prediction} risk. "

            f"The assessment indicates that the project should "
            f"be managed according to its identified risk factors "
            f"while continuing to monitor project execution."
        )


        # =====================================================
        # RISK FACTOR DATA
        # =====================================================

        risk_factors = [

            {
                "name": "Team Size",
                "level": risk["team_level"],
                "percent": risk["team_percent"]
            },

            {
                "name": "Budget",
                "level": risk["budget_level"],
                "percent": risk["budget_percent"]
            },

            {
                "name": "Timeline",
                "level": risk["timeline_level"],
                "percent": risk["timeline_percent"]
            },

            {
                "name": "Technology",
                "level": risk["technology_level"],
                "percent": risk["technology_percent"]
            }

        ]


        # =====================================================
        # RETURN REPORT DATA
        # =====================================================

        return {

            "rating": rating,

            "verdict": verdict,

            "summary": summary,

            "ml_prediction": ml_prediction,

            "success_probability":
                success_probability,

            "risk_factors":
                risk_factors

        }