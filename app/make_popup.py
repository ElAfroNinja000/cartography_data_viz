from bs4 import BeautifulSoup


# We're using the BeautifulSoup library to parse the HTML string that we've already created, and then we're adding a new
# row to the table for each metric that we want to display
class PopupMaker:
    """
    This function takes in a country and a list of metrics and creates an html table with the country as the header and
    the metrics as the rows

    :param country: the name of the country
    :param metrics: a list of metrics to be displayed in the table
    """
    def __init__(self, country, metrics):
        self.country = country
        self.metrics = metrics
        self.html = f"""<!DOCTYPE html>
                        <html>
                          <head>
                            <h4 style="margin-bottom:10"; width="200px">{country}</h4>
                          </head>
                          <table style="height: 126px; width: 350px;">
                           <tbody>
                           </tbody>
                          </table>
                        </html>
                        """

    """
    This function parses the HTML string that we've already created, and then we're adding a
    new row to the table for each metric that we want to display
    :return: The html code for the popup.
    """
    def make_html_popup(self):
        soup = BeautifulSoup(self.html, "html.parser")
        body = soup.select("tbody")
        for i, metric in enumerate(self.metrics):
            metric_tr = soup.new_tag("tr")
            field_td  = soup.new_tag('td')
            value_td  = soup.new_tag('td')

            if i % 2 == 1:
                metric_tr.attrs["bgcolor"] = "#d4d4d4"
            field_td.string = metric
            value_td.string = str(self.metrics[metric])

            metric_tr.append(field_td)
            metric_tr.append(value_td)
            body[0].append(metric_tr)
        return soup.prettify()
