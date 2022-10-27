import { AppComponent } from '../app.component';
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Record } from '../record';
import * as d3 from 'd3';

@Component({
  selector: 'app-bar',
  templateUrl: './bar.component.html',
  styleUrls: ['./bar.component.scss'],
})
export class BarComponent extends AppComponent implements OnInit {
  private colleges: string[] = [];
  private svg;
  private margin = 50;
  private width = 1000 - (this.margin * 2);
  private height = 500 - (this.margin * 2);

  constructor(http: HttpClient) {
    super(http);
    http.get('../assets/records.json').subscribe(data => {
      this.records = data as Record[];
      this.colleges = Array.from(new Set<string>(this.records.map(record => record.college)));
      console.log(this.colleges);
      this.drawBars(this.colleges);
    });
  }

  override ngOnInit(): void {
    this.createSvg();
  }

  // graph template
  private createSvg(): void {
    this.svg = d3.select("figure#bar")
    .append("svg")
    .attr("width", this.width + (this.margin * 2) + 200)
    .attr("height", this.height + (this.margin * 2) + 200)
    .append("g")
    .attr("transform", "translate(" + this.margin + "," + this.margin + ")");
  }

  private drawBars(data: any[]): void {
    // Create the X-axis band scale
    const x = d3.scaleBand()
    .range([0, this.width])
    .domain(this.colleges)
    .padding(0.2);

    // Draw the X-axis on the DOM
    this.svg.append("g")
    .attr("transform", "translate(0," + this.height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

    // Create the Y-axis band scale
    const y = d3.scaleLinear()
    .domain([0, 200000])
    .range([this.height, 0]);

    // Draw the Y-axis on the DOM
    this.svg.append("g")
    .call(d3.axisLeft(y));

    // Create and fill the bars
    this.svg.selectAll("bars")
    .data(data)
    .enter()
    .append("rect")
    //.attr("x", d => x(d.college))
    //.attr("y", d => y(d.salary))
    .attr("width", x.bandwidth())
    //.attr("height", (d) => this.height - y(d.salary))
    .attr("fill", "#d04a35");
  }

}
