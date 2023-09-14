import { ChangeDetectorRef, Component } from '@angular/core';
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
  messageList : ElementDto[] = []

  constructor(private frontendService: DrawFrontendService, private cd: ChangeDetectorRef) {}


  ngAfterViewInit(): void {

    this.frontendService.menuBar.subscribe({next: data => {
      // Explicitly set to null and then to data (again), as otherwise typescript doesn't get it that a change occurred...
      this.menuBar = null
      this.cd.detectChanges()
      this.menuBar = data
      this.cd.detectChanges()
    }})

  }
}
