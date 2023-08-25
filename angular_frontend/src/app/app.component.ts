import { Component } from '@angular/core';
import { DrawFrontendService } from './draw-frontend.service';
import { ElementDto } from './types/json-response.dto';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Clinguin';

  menuBar : ElementDto | null = null

  constructor(private frontendService: DrawFrontendService) {}


  ngAfterViewInit(): void {

    this.frontendService.menuBar.subscribe({next: data => {
      this.menuBar = data
    }})
  }
}
