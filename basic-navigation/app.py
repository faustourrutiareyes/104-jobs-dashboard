import seaborn as sns

# Import data from shared.py
from shared import app_dir, languages, jobs
from shiny.express import input, render, ui

ui.page_opts(title="104 Software Jobs", fillable= True)

ui.nav_spacer()  # Push the navbar items to the right

with ui.nav_panel("Jobs"):

    with ui.card(): 
    
        with ui.layout_sidebar():    
            with ui.sidebar():
                ui.input_selectize(
                    "selected_cities",
                    "City",
                    list(jobs["County City"].unique()),
                    selected=["Taipei City", "New Taipei City"],
                    multiple=True,
                )

                ui.input_selectize(
                    "edu_level",
                    "Highest Education Level",
                    ['Not Specified',"Highschool", "Technical school", "Undergraduate", "Master's", "PhD"],
                    selected=["Not Specified"],
                    multiple=False,
                )

                ui.input_selectize(
                    "full_part_time",
                    "Work Type",
                    ["Full-time", "Part-time"],
                    selected=["Full-time"],
                    multiple=False,
                )
                
                ui.input_selectize(
                    "selected_languages_jobs",
                    "Language",
                    list(languages["Language"].unique()),
                    multiple=True)
            
            @render.data_frame
            def jobs_df():
                jobs_filtered = jobs.drop(columns=['Working Experience'])
                if 'Not Specified' not in input.edu_level():
                    jobs_filtered = jobs_filtered[
                        jobs_filtered["Education Requirements"].str.contains(input.edu_level())
                    ]
                jobs_filtered = jobs_filtered[
                    jobs_filtered["Work Nature"].str.contains(input.full_part_time())
                ]
                if input.selected_cities():
                    jobs_filtered = jobs_filtered[
                        jobs_filtered["County City"].isin(input.selected_cities())
                    ]
                if input.selected_languages_jobs():
                    jobs_filtered = jobs_filtered[
                        jobs_filtered["Proficiency in tools"].str.contains("|".join(list(input.selected_languages_jobs())))
                    ]
                return render.DataGrid(jobs_filtered, filters=True)


with ui.nav_panel("Languages in Demand"):
    
    ui.input_selectize(
        "selected_languages",
        "Language",
        list(languages["Language"].unique()),
        multiple=True)

    @render.plot
    def language_plot():
        sns.set_theme(style="whitegrid")
        colors = [
            "blue" if lang in input.selected_languages() else "gray"
            for lang in languages["Language"]
        ]
        plot = sns.barplot(
            y="Language",
            x="PercentageString",
            data=languages,
            color="gray",
            orient="h",
            palette=colors,
        )
        plot.set(xlabel="%", ylabel="Language")

        return plot

    @render.text
    def selected_languages_text():
        return f"Selected languages: {', '.join(input.selected_languages())}"

