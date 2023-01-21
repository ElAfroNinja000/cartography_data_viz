from bs4 import BeautifulSoup


class PopupMaker:
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

    def make_html_popup(self):
        soup = BeautifulSoup(self.html, "html")
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
