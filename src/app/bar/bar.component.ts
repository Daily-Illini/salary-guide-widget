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
  /* graph data */
  private salaries: Object[] = [];
  private maxSalary: number;
  /* graph container dimensions */
  private svg;
  private margin = 50;
  private width = 1000 - (this.margin * 2);
  private height = 500 - (this.margin * 2);

  constructor(http: HttpClient) {
    super(http);
    http.get('../assets/records.json').subscribe(data => {
      this.records = data as Record[];
      this.getSalaries();
      this.drawBars(this.salaries);
    });
  }

  override ngOnInit(): void {
    this.createSvg();
  }

  // retrieves total salary budget for each college
  private getSalaries(): void {
    var maxSalary: number = 0;
    var colleges: string[] = Array.from(new Set<string>(this.records.map(record => record.college)));
    for (var i = 0; i < colleges.length; i++) {
      var collegeSalary = 0;
      for (const r of this.records) {
        if (colleges[i] == r.college) {
          collegeSalary += Number(r.salary.replace(/[^0-9.-]+/g,""));
        }
        maxSalary = Math.max(maxSalary, collegeSalary);
      }
      collegeSalary /= 1000000; // scaling
      this.salaries.push({name : colleges[i], college : collegeSalary.toString()});
    }
    this.maxSalary = maxSalary / 1000000; // scaling
    console.log(this.maxSalary);
    console.log(this.salaries);
  }

  // draw graph container
  private createSvg(): void {
    this.svg = d3.select("figure#bar")
    .append("svg")
    .attr("width", this.width + (this.margin * 2) + 200)
    .attr("height", this.height + (this.margin * 2) + 200)
    .append("g")
    .attr("transform", "translate(" + this.margin + "," + this.margin + ")");
  }

  // draws bar graph
  private drawBars(data: any[]): void {
    // Create the X-axis band scale
    const x = d3.scaleBand()
    .range([0, this.width])
    .domain(data.map(d => d.name))
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
    .domain([0, this.maxSalary])
    .range([this.height, 0]);

    // Draw the Y-axis on the DOM
    this.svg.append("g")
    .call(d3.axisLeft(y));

    // Create and fill the bars
    this.svg.selectAll("bars")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", d => x(d.name))
    .attr("y", d => y(d.college))
    .attr("width", x.bandwidth())
    .attr("height", (d) => this.height - y(d.college))
    .attr("fill", "#FF5F05");
  }
}
