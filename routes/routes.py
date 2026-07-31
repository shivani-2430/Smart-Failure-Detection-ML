from flask import render_template, request, redirect, url_for, send_file

from database.db import db
from models.project import Project

from services.risk_service import RiskService
from services.market_service import MarketService
from services.recommendation_service import RecommendationService
from services.report_service import ReportService

import io

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def register_routes(app):

    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/submit", methods=["POST"])
    def submit():

        project = Project(
            project_name=request.form.get("project_name"),
            organization=request.form.get("organization"),
            domain=request.form.get("domain"),
            tech_stack=request.form.get("tech_stack"),

            team_size=request.form.get("team_size"),
            budget=request.form.get("budget"),
            timeline=request.form.get("timeline"),

            description=request.form.get("description")
        )

        db.session.add(project)
        db.session.commit()

        return redirect(url_for("risk"))
    @app.route("/decision-simulator")
    def decision_simulator():

        project = Project.query.order_by(Project.id.desc()).first()

        if project is None:
            return redirect(url_for("risk"))

        projects = Project.query.all()

        risk = RiskService.calculate_risk(project)

        total_projects = len(projects)

        unique_domains = len(
            set(
                p.domain
                for p in projects
                if p.domain
            )
        )

        reports_generated = total_projects

        metrics = {

            "budget": project.budget,

            "timeline": project.timeline,

            "team_size": project.team_size,

            "technology_count": len(project.tech_stack.split(","))

        }

        return render_template(

            "analytics.html",

            project=project,

            latest_project=project,

            risk=risk,

            metrics=metrics,

            projects=projects,

            total_projects=total_projects,

            unique_domains=unique_domains,

            reports_generated=reports_generated

        )
    @app.route("/project/<int:id>")
    def view_project(id):

        project = Project.query.get_or_404(id)

        return render_template(
            "view_project.html",
            project=project
        )
    @app.route("/delete/<int:id>")
    def delete_project(id):

        project = Project.query.get_or_404(id)

        db.session.delete(project)
        db.session.commit()

        return redirect(url_for("home"))
    @app.route("/edit/<int:id>")
    def edit_project(id):

        project = Project.query.get_or_404(id)

        return render_template(
            "edit_project.html",
            project=project
        )


    @app.route("/update/<int:id>", methods=["POST"])
    def update_project(id):

        project = Project.query.get_or_404(id)

        project.project_name = request.form.get("project_name")
        project.organization = request.form.get("organization")
        project.domain = request.form.get("domain")
        project.tech_stack = request.form.get("tech_stack")

        project.team_size = request.form.get("team_size")
        project.budget = request.form.get("budget")
        project.timeline = request.form.get("timeline")

        project.description = request.form.get("description")

        db.session.commit()

        return redirect(url_for("risk"))


    @app.route("/risk")
    def risk():

        project = Project.query.order_by(Project.id.desc()).first()

        if project is None:
            return render_template(
                "risk.html",
                project=None,
                risk_score=0,
                risk_level="NO DATA",
                summary="No project available.",
                team_level="LOW",
                budget_level="LOW",
                timeline_level="LOW",
                technology_level="LOW",
                team_percent=0,
                budget_percent=0,
                timeline_percent=0,
                technology_percent=0
            )

        result = RiskService.calculate_risk(project)

        return render_template(
            "risk.html",
            project=project,
            risk_score=result["score"],
            risk_level=result["level"],
            summary=result["summary"],
            team_level=result["team_level"],
            budget_level=result["budget_level"],
            timeline_level=result["timeline_level"],
            technology_level=result["technology_level"],
            team_percent=result["team_percent"],
            budget_percent=result["budget_percent"],
            timeline_percent=result["timeline_percent"],
            technology_percent=result["technology_percent"]
        )
    @app.route("/recommendation")
    def recommendations():

        project = Project.query.order_by(Project.id.desc()).first()

        if project is None:

            return redirect(url_for("home"))

        risk = RiskService.calculate_risk(project)

        from services.recommendation_service import RecommendationService

        recommendation = RecommendationService.generate(
            project,
            risk
        )

        return render_template(

            "recommendation.html",

            project=project,

            health=recommendation["health"],

            success_probability=recommendation["success_probability"],

            priority_actions=recommendation["priority_actions"],

            technologies=recommendation["technologies"],

            mitigation=recommendation["mitigation"],

            summary=recommendation["summary"]

        )
    @app.route("/market")
    def market():

        project = Project.query.order_by(Project.id.desc()).first()

        if project is None:
            return redirect(url_for("home"))

        from services.market_service import MarketService

        market_data = MarketService.generate(project)

        return render_template(

            "market.html",

            project=project,

            industry=market_data["industry"],

            demand=market_data["demand"],

            growth=market_data["growth"],

            competitors=market_data["competitors"],

            swot=market_data["swot"],

            insights=market_data["insights"]

        )
    @app.route("/report")
    def report():

        project = Project.query.order_by(Project.id.desc()).first()

        if project is None:
            return redirect(url_for("home"))

        risk = RiskService.calculate_risk(project)

        from services.recommendation_service import RecommendationService
        recommendation = RecommendationService.generate(project, risk)

        from services.market_service import MarketService
        market = MarketService.generate(project)

        from services.report_service import ReportService
        report_data = ReportService.generate(
            project,
            risk,
            recommendation,
            market
        )

        return render_template(

            "report.html",

            project=project,

            risk=risk,

            recommendation=recommendation,

            market=market,

            rating=report_data["rating"],

            verdict=report_data["verdict"],

            summary=report_data["summary"]

        )
    @app.route("/download-report")
    def download_report():

        project = Project.query.order_by(Project.id.desc()).first()

        if project is None:
            return redirect(url_for("home"))

        risk = RiskService.calculate_risk(project)

        from services.recommendation_service import RecommendationService
        recommendation = RecommendationService.generate(project, risk)

        from services.market_service import MarketService
        market = MarketService.generate(project)

        from services.report_service import ReportService
        report_data = ReportService.generate(
            project,
            risk,
            recommendation,
            market
        )

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(Paragraph("<b>Executive Project Report</b>", styles["Title"]))

        story.append(Paragraph(f"<b>Project Name:</b> {project.project_name}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Domain:</b> {project.domain}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Technology:</b> {project.tech_stack}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Budget:</b> {project.budget}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Timeline:</b> {project.timeline} Months", styles["BodyText"]))
        story.append(Paragraph(f"<b>Team Size:</b> {project.team_size}", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Risk Assessment</b>", styles["Heading2"]))
        story.append(Paragraph(f"Risk Score : {risk['score']}", styles["BodyText"]))
        story.append(Paragraph(f"Risk Level : {risk['level']}", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>AI Recommendation</b>", styles["Heading2"]))
        story.append(Paragraph(f"Project Health : {recommendation['health']}", styles["BodyText"]))
        story.append(Paragraph(f"Success Probability : {recommendation['success_probability']}%", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Market Intelligence</b>", styles["Heading2"]))
        story.append(Paragraph(f"Industry : {market['industry']}", styles["BodyText"]))
        story.append(Paragraph(f"Market Demand : {market['demand']}", styles["BodyText"]))
        story.append(Paragraph(f"Growth : {market['growth']}", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Overall Evaluation</b>", styles["Heading2"]))
        story.append(Paragraph(f"Rating : {report_data['rating']}", styles["BodyText"]))
        story.append(Paragraph(f"Verdict : {report_data['verdict']}", styles["BodyText"]))
        story.append(Paragraph(report_data["summary"], styles["BodyText"]))

        doc.build(story)

        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="Executive_Report.pdf",
            mimetype="application/pdf"
        )