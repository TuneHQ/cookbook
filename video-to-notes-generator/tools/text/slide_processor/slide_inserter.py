from tools.text.slide_processor.note_slide_mapper import SlidePlacementProcessor


class SlideInserter:
    def __init__(self, notes, slides) -> None:
        self.notes = notes
        self.slides = slides

    def insert_slides(self) -> str:
        slide_processor = SlidePlacementProcessor(self.notes, self.slides)
        slide_locations = slide_processor.process_notes()

        # Split notes by new lines
        lines = self.notes.split("\n")
        for number, location in slide_locations.items():
            # Insert slide at location in lines
            lines.insert(location, f"[slide {number}]")
        # Join lines by new lines
        return "\n".join(lines)


# Usage
if __name__ == "__main__":
    notes_content = """
    # Introduction to Machine Learning
    Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to "learn" from data, without being explicitly programmed.

    ## Supervised Learning
    Supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs.

    ### Linear Regression
    Linear regression is a linear approach to modeling the relationship between a dependent variable and one or more independent variables.

    ### Classification
    Classification is the problem of identifying to which of a set of categories a new observation belongs, on the basis of a training set of data containing observations whose category membership is known.

    ## Unsupervised Learning
    Unsupervised learning is a type of machine learning algorithm used to draw inferences from datasets consisting of input data without labeled responses.

    ### Clustering
    Clustering is the task of dividing the population or data points into a number of groups such that data points in the same groups are more similar to other data points in the same group than those in other groups.

    ### Dimensionality Reduction
    Dimensionality reduction is the process of reducing the number of random variables under consideration by obtaining a set of principal variables.
    """
    slides = {
        1: "Introduction to Machine Learning",
        2: "Supervised Learning",
        3: "Linear Regression",
        4: "Classification",
        5: "Unsupervised Learning",
        6: "Clustering",
        7: "Dimensionality Reduction",
    }
    inserter = SlideInserter(notes_content, slides)
    updated_notes = inserter.insert_slides()
    print(updated_notes)
