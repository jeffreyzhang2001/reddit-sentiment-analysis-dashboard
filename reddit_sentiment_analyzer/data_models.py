#Need to add sentiment attributes to each model
#Need to store scraped data in objects

#Model representing a submission
class SubmissionModel():
    def __init__(self, title, author, timestamp, submission_id):
        self.title = title
        self.author = author
        self.timestamp = timestamp
        self.submission_id = submission_id

    def generate_submission_dictionary(self):
        submission_dict = {'title':self.title, 
                           'author':self.author,
                           'timestamp':self.timestamp,
                           'submission_id':self.submission_id}
        return submission_dict

#Model representing a comment
class CommentModel():
    def __init__(self, submission, comment_text, author, timestamp, stickied):
        #Each comment is linked to a corresponding submission object
        self.submission = submission
        self.comment_text = comment_text
        self.author = author
        self.timestamp = timestamp
        self.stickied = stickied

    def generate_comment_dictionary(self):
        comment_dict = {'submission':self.submission,
                        'comment_text':self.comment_text,
                        'author':self.author,
                        'timestamp':self.timestamp,
                        'stickied':self.stickied}
        return comment_dict

