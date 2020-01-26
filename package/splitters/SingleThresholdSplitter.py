from .AbstractSplitter import AbstractSplitter


class SingleThresholdSplitter(AbstractSplitter):
    estimates = []
    threshold = 0.0
    split_points = []

    def __init__(self, estimates, threshold):
        self.estimates = estimates
        self.threshold = threshold

        self.split_points = [
            index + 1
            for index, value
            in enumerate(self.estimates)
            if value < self.threshold
        ]

    def split_document(self, lines_in_document):
        sections = []

        prev_split_point = 0
        for current_split_point in self.split_points:
            section = lines_in_document[prev_split_point:current_split_point]
            sections.append('\n'.join(section))

            prev_split_point = current_split_point

        sections.append('\n'.join(lines_in_document[prev_split_point:]))

        return sections
