class RecommendationService:

    @staticmethod
    def generate(project, risk):

        score = risk["score"]

        # ----------------------------
        # Project Health
        # ----------------------------

        if score >= 70:
            health = "Critical"

        elif score >= 40:
            health = "Moderate"

        else:
            health = "Healthy"

        # ----------------------------
        # Success Probability
        # ----------------------------

        success_probability = max(10, 100 - score)

        # ----------------------------
        # Priority Actions
        # ----------------------------

        priority_actions = []

        if int(project.budget) < 500000:
            priority_actions.append("Increase Budget")

        if int(project.team_size) < 5:
            priority_actions.append("Hire More Developers")

        if int(project.timeline) < 6:
            priority_actions.append("Extend Timeline")

        if len(priority_actions) == 0:
            priority_actions.append("Continue Current Plan")

        # ----------------------------
        # Recommended Technologies
        # ----------------------------

        technologies = []

        tech = project.tech_stack.lower()

        if "java" in tech:
            technologies.extend([
                "Docker",
                "Swagger",
                "JUnit",
                "Postman"
            ])

        elif "python" in tech:

            technologies.extend([
                "FastAPI",
                "Docker",
                "Pandas",
                "MLflow"
            ])

        else:

            technologies.extend([
                "Docker",
                "Git",
                "Postman",
                "CI/CD"
            ])

        # ----------------------------
        # Risk Mitigation
        # ----------------------------

        mitigation = [

            "Weekly Sprint Review",

            "Automated Testing",

            "Daily Backup",

            "Security Audit"

        ]

        # ----------------------------
        # AI Summary
        # ----------------------------

        summary = (
            f"The project has a {health.lower()} health status with an "
            f"estimated success probability of {success_probability}%. "
            "Increasing available resources, following agile practices, "
            "and adopting recommended technologies will improve project "
            "delivery and reduce overall risk."
        )

        return {

            "health": health,

            "success_probability": success_probability,

            "priority_actions": priority_actions,

            "technologies": technologies,

            "mitigation": mitigation,

            "summary": summary

        }