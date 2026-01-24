/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 4.0, "minX": 0.0, "maxY": 323.0, "series": [{"data": [[0.0, 4.0], [0.1, 4.0], [0.2, 4.0], [0.3, 4.0], [0.4, 4.0], [0.5, 4.0], [0.6, 4.0], [0.7, 4.0], [0.8, 4.0], [0.9, 5.0], [1.0, 5.0], [1.1, 5.0], [1.2, 5.0], [1.3, 5.0], [1.4, 5.0], [1.5, 5.0], [1.6, 5.0], [1.7, 5.0], [1.8, 5.0], [1.9, 5.0], [2.0, 5.0], [2.1, 5.0], [2.2, 5.0], [2.3, 5.0], [2.4, 5.0], [2.5, 5.0], [2.6, 5.0], [2.7, 5.0], [2.8, 5.0], [2.9, 5.0], [3.0, 5.0], [3.1, 5.0], [3.2, 5.0], [3.3, 5.0], [3.4, 5.0], [3.5, 5.0], [3.6, 5.0], [3.7, 5.0], [3.8, 5.0], [3.9, 5.0], [4.0, 5.0], [4.1, 5.0], [4.2, 5.0], [4.3, 5.0], [4.4, 5.0], [4.5, 5.0], [4.6, 5.0], [4.7, 5.0], [4.8, 5.0], [4.9, 5.0], [5.0, 5.0], [5.1, 5.0], [5.2, 5.0], [5.3, 5.0], [5.4, 5.0], [5.5, 5.0], [5.6, 5.0], [5.7, 6.0], [5.8, 6.0], [5.9, 6.0], [6.0, 6.0], [6.1, 6.0], [6.2, 6.0], [6.3, 6.0], [6.4, 6.0], [6.5, 6.0], [6.6, 6.0], [6.7, 6.0], [6.8, 6.0], [6.9, 6.0], [7.0, 6.0], [7.1, 6.0], [7.2, 6.0], [7.3, 6.0], [7.4, 6.0], [7.5, 6.0], [7.6, 6.0], [7.7, 6.0], [7.8, 6.0], [7.9, 6.0], [8.0, 6.0], [8.1, 6.0], [8.2, 6.0], [8.3, 6.0], [8.4, 6.0], [8.5, 6.0], [8.6, 6.0], [8.7, 6.0], [8.8, 6.0], [8.9, 6.0], [9.0, 6.0], [9.1, 6.0], [9.2, 6.0], [9.3, 6.0], [9.4, 6.0], [9.5, 6.0], [9.6, 6.0], [9.7, 6.0], [9.8, 6.0], [9.9, 6.0], [10.0, 6.0], [10.1, 6.0], [10.2, 6.0], [10.3, 6.0], [10.4, 6.0], [10.5, 6.0], [10.6, 6.0], [10.7, 6.0], [10.8, 6.0], [10.9, 6.0], [11.0, 6.0], [11.1, 6.0], [11.2, 6.0], [11.3, 6.0], [11.4, 6.0], [11.5, 6.0], [11.6, 6.0], [11.7, 6.0], [11.8, 6.0], [11.9, 6.0], [12.0, 6.0], [12.1, 6.0], [12.2, 6.0], [12.3, 6.0], [12.4, 6.0], [12.5, 6.0], [12.6, 6.0], [12.7, 6.0], [12.8, 6.0], [12.9, 6.0], [13.0, 6.0], [13.1, 6.0], [13.2, 6.0], [13.3, 6.0], [13.4, 7.0], [13.5, 7.0], [13.6, 7.0], [13.7, 7.0], [13.8, 7.0], [13.9, 7.0], [14.0, 7.0], [14.1, 7.0], [14.2, 7.0], [14.3, 7.0], [14.4, 7.0], [14.5, 7.0], [14.6, 7.0], [14.7, 7.0], [14.8, 7.0], [14.9, 7.0], [15.0, 7.0], [15.1, 7.0], [15.2, 7.0], [15.3, 7.0], [15.4, 7.0], [15.5, 7.0], [15.6, 7.0], [15.7, 7.0], [15.8, 7.0], [15.9, 7.0], [16.0, 7.0], [16.1, 7.0], [16.2, 7.0], [16.3, 7.0], [16.4, 7.0], [16.5, 7.0], [16.6, 7.0], [16.7, 7.0], [16.8, 7.0], [16.9, 7.0], [17.0, 7.0], [17.1, 7.0], [17.2, 7.0], [17.3, 7.0], [17.4, 7.0], [17.5, 7.0], [17.6, 7.0], [17.7, 7.0], [17.8, 7.0], [17.9, 7.0], [18.0, 7.0], [18.1, 7.0], [18.2, 7.0], [18.3, 7.0], [18.4, 7.0], [18.5, 7.0], [18.6, 7.0], [18.7, 7.0], [18.8, 7.0], [18.9, 7.0], [19.0, 7.0], [19.1, 7.0], [19.2, 7.0], [19.3, 7.0], [19.4, 7.0], [19.5, 7.0], [19.6, 7.0], [19.7, 7.0], [19.8, 7.0], [19.9, 7.0], [20.0, 7.0], [20.1, 7.0], [20.2, 7.0], [20.3, 7.0], [20.4, 7.0], [20.5, 7.0], [20.6, 7.0], [20.7, 7.0], [20.8, 7.0], [20.9, 7.0], [21.0, 7.0], [21.1, 8.0], [21.2, 8.0], [21.3, 8.0], [21.4, 8.0], [21.5, 8.0], [21.6, 8.0], [21.7, 8.0], [21.8, 8.0], [21.9, 8.0], [22.0, 8.0], [22.1, 8.0], [22.2, 8.0], [22.3, 8.0], [22.4, 8.0], [22.5, 8.0], [22.6, 8.0], [22.7, 8.0], [22.8, 8.0], [22.9, 8.0], [23.0, 8.0], [23.1, 8.0], [23.2, 8.0], [23.3, 8.0], [23.4, 8.0], [23.5, 8.0], [23.6, 8.0], [23.7, 8.0], [23.8, 8.0], [23.9, 8.0], [24.0, 8.0], [24.1, 8.0], [24.2, 8.0], [24.3, 8.0], [24.4, 8.0], [24.5, 8.0], [24.6, 8.0], [24.7, 8.0], [24.8, 8.0], [24.9, 8.0], [25.0, 8.0], [25.1, 8.0], [25.2, 8.0], [25.3, 8.0], [25.4, 8.0], [25.5, 8.0], [25.6, 8.0], [25.7, 8.0], [25.8, 8.0], [25.9, 8.0], [26.0, 8.0], [26.1, 8.0], [26.2, 8.0], [26.3, 8.0], [26.4, 8.0], [26.5, 8.0], [26.6, 8.0], [26.7, 8.0], [26.8, 8.0], [26.9, 8.0], [27.0, 8.0], [27.1, 8.0], [27.2, 8.0], [27.3, 8.0], [27.4, 8.0], [27.5, 8.0], [27.6, 8.0], [27.7, 8.0], [27.8, 8.0], [27.9, 8.0], [28.0, 8.0], [28.1, 8.0], [28.2, 8.0], [28.3, 8.0], [28.4, 8.0], [28.5, 8.0], [28.6, 8.0], [28.7, 8.0], [28.8, 8.0], [28.9, 8.0], [29.0, 8.0], [29.1, 8.0], [29.2, 8.0], [29.3, 8.0], [29.4, 8.0], [29.5, 8.0], [29.6, 8.0], [29.7, 8.0], [29.8, 8.0], [29.9, 8.0], [30.0, 8.0], [30.1, 8.0], [30.2, 8.0], [30.3, 8.0], [30.4, 8.0], [30.5, 8.0], [30.6, 9.0], [30.7, 9.0], [30.8, 9.0], [30.9, 9.0], [31.0, 9.0], [31.1, 9.0], [31.2, 9.0], [31.3, 9.0], [31.4, 9.0], [31.5, 9.0], [31.6, 9.0], [31.7, 9.0], [31.8, 9.0], [31.9, 9.0], [32.0, 9.0], [32.1, 9.0], [32.2, 9.0], [32.3, 9.0], [32.4, 9.0], [32.5, 9.0], [32.6, 9.0], [32.7, 9.0], [32.8, 9.0], [32.9, 9.0], [33.0, 9.0], [33.1, 9.0], [33.2, 9.0], [33.3, 9.0], [33.4, 9.0], [33.5, 9.0], [33.6, 9.0], [33.7, 9.0], [33.8, 9.0], [33.9, 9.0], [34.0, 9.0], [34.1, 9.0], [34.2, 9.0], [34.3, 9.0], [34.4, 9.0], [34.5, 9.0], [34.6, 9.0], [34.7, 9.0], [34.8, 9.0], [34.9, 9.0], [35.0, 9.0], [35.1, 9.0], [35.2, 9.0], [35.3, 9.0], [35.4, 9.0], [35.5, 9.0], [35.6, 9.0], [35.7, 9.0], [35.8, 9.0], [35.9, 9.0], [36.0, 9.0], [36.1, 9.0], [36.2, 9.0], [36.3, 9.0], [36.4, 9.0], [36.5, 9.0], [36.6, 9.0], [36.7, 9.0], [36.8, 9.0], [36.9, 9.0], [37.0, 9.0], [37.1, 9.0], [37.2, 9.0], [37.3, 9.0], [37.4, 9.0], [37.5, 9.0], [37.6, 9.0], [37.7, 9.0], [37.8, 9.0], [37.9, 9.0], [38.0, 9.0], [38.1, 9.0], [38.2, 9.0], [38.3, 9.0], [38.4, 9.0], [38.5, 10.0], [38.6, 10.0], [38.7, 10.0], [38.8, 10.0], [38.9, 10.0], [39.0, 10.0], [39.1, 10.0], [39.2, 10.0], [39.3, 10.0], [39.4, 10.0], [39.5, 10.0], [39.6, 10.0], [39.7, 10.0], [39.8, 10.0], [39.9, 10.0], [40.0, 10.0], [40.1, 10.0], [40.2, 10.0], [40.3, 10.0], [40.4, 10.0], [40.5, 10.0], [40.6, 10.0], [40.7, 10.0], [40.8, 10.0], [40.9, 10.0], [41.0, 10.0], [41.1, 10.0], [41.2, 10.0], [41.3, 10.0], [41.4, 10.0], [41.5, 10.0], [41.6, 10.0], [41.7, 10.0], [41.8, 10.0], [41.9, 10.0], [42.0, 10.0], [42.1, 10.0], [42.2, 10.0], [42.3, 10.0], [42.4, 10.0], [42.5, 10.0], [42.6, 10.0], [42.7, 10.0], [42.8, 10.0], [42.9, 10.0], [43.0, 10.0], [43.1, 10.0], [43.2, 10.0], [43.3, 10.0], [43.4, 10.0], [43.5, 10.0], [43.6, 10.0], [43.7, 11.0], [43.8, 11.0], [43.9, 11.0], [44.0, 11.0], [44.1, 11.0], [44.2, 11.0], [44.3, 11.0], [44.4, 11.0], [44.5, 11.0], [44.6, 11.0], [44.7, 11.0], [44.8, 11.0], [44.9, 11.0], [45.0, 11.0], [45.1, 11.0], [45.2, 11.0], [45.3, 11.0], [45.4, 11.0], [45.5, 11.0], [45.6, 11.0], [45.7, 11.0], [45.8, 11.0], [45.9, 11.0], [46.0, 11.0], [46.1, 11.0], [46.2, 11.0], [46.3, 11.0], [46.4, 11.0], [46.5, 11.0], [46.6, 11.0], [46.7, 11.0], [46.8, 11.0], [46.9, 11.0], [47.0, 11.0], [47.1, 11.0], [47.2, 11.0], [47.3, 11.0], [47.4, 11.0], [47.5, 11.0], [47.6, 11.0], [47.7, 11.0], [47.8, 11.0], [47.9, 11.0], [48.0, 11.0], [48.1, 11.0], [48.2, 11.0], [48.3, 11.0], [48.4, 11.0], [48.5, 11.0], [48.6, 11.0], [48.7, 11.0], [48.8, 11.0], [48.9, 11.0], [49.0, 11.0], [49.1, 11.0], [49.2, 12.0], [49.3, 12.0], [49.4, 12.0], [49.5, 12.0], [49.6, 12.0], [49.7, 12.0], [49.8, 12.0], [49.9, 12.0], [50.0, 12.0], [50.1, 12.0], [50.2, 12.0], [50.3, 12.0], [50.4, 12.0], [50.5, 12.0], [50.6, 12.0], [50.7, 12.0], [50.8, 12.0], [50.9, 12.0], [51.0, 12.0], [51.1, 12.0], [51.2, 12.0], [51.3, 12.0], [51.4, 12.0], [51.5, 12.0], [51.6, 12.0], [51.7, 12.0], [51.8, 12.0], [51.9, 12.0], [52.0, 12.0], [52.1, 12.0], [52.2, 12.0], [52.3, 12.0], [52.4, 12.0], [52.5, 12.0], [52.6, 12.0], [52.7, 12.0], [52.8, 12.0], [52.9, 13.0], [53.0, 13.0], [53.1, 13.0], [53.2, 13.0], [53.3, 13.0], [53.4, 13.0], [53.5, 13.0], [53.6, 13.0], [53.7, 13.0], [53.8, 13.0], [53.9, 13.0], [54.0, 13.0], [54.1, 13.0], [54.2, 13.0], [54.3, 13.0], [54.4, 13.0], [54.5, 13.0], [54.6, 13.0], [54.7, 13.0], [54.8, 13.0], [54.9, 13.0], [55.0, 13.0], [55.1, 13.0], [55.2, 13.0], [55.3, 13.0], [55.4, 13.0], [55.5, 14.0], [55.6, 14.0], [55.7, 14.0], [55.8, 14.0], [55.9, 14.0], [56.0, 14.0], [56.1, 14.0], [56.2, 14.0], [56.3, 14.0], [56.4, 14.0], [56.5, 14.0], [56.6, 14.0], [56.7, 14.0], [56.8, 14.0], [56.9, 14.0], [57.0, 14.0], [57.1, 14.0], [57.2, 14.0], [57.3, 14.0], [57.4, 14.0], [57.5, 14.0], [57.6, 14.0], [57.7, 14.0], [57.8, 14.0], [57.9, 14.0], [58.0, 15.0], [58.1, 15.0], [58.2, 15.0], [58.3, 15.0], [58.4, 15.0], [58.5, 15.0], [58.6, 15.0], [58.7, 15.0], [58.8, 15.0], [58.9, 15.0], [59.0, 15.0], [59.1, 15.0], [59.2, 15.0], [59.3, 15.0], [59.4, 15.0], [59.5, 15.0], [59.6, 15.0], [59.7, 15.0], [59.8, 15.0], [59.9, 15.0], [60.0, 15.0], [60.1, 15.0], [60.2, 15.0], [60.3, 15.0], [60.4, 16.0], [60.5, 16.0], [60.6, 16.0], [60.7, 16.0], [60.8, 16.0], [60.9, 16.0], [61.0, 16.0], [61.1, 16.0], [61.2, 16.0], [61.3, 16.0], [61.4, 16.0], [61.5, 16.0], [61.6, 16.0], [61.7, 16.0], [61.8, 16.0], [61.9, 16.0], [62.0, 16.0], [62.1, 17.0], [62.2, 17.0], [62.3, 17.0], [62.4, 17.0], [62.5, 17.0], [62.6, 17.0], [62.7, 17.0], [62.8, 17.0], [62.9, 17.0], [63.0, 17.0], [63.1, 17.0], [63.2, 17.0], [63.3, 17.0], [63.4, 18.0], [63.5, 18.0], [63.6, 18.0], [63.7, 18.0], [63.8, 18.0], [63.9, 18.0], [64.0, 18.0], [64.1, 18.0], [64.2, 18.0], [64.3, 18.0], [64.4, 18.0], [64.5, 18.0], [64.6, 18.0], [64.7, 19.0], [64.8, 19.0], [64.9, 19.0], [65.0, 19.0], [65.1, 19.0], [65.2, 19.0], [65.3, 19.0], [65.4, 20.0], [65.5, 20.0], [65.6, 20.0], [65.7, 20.0], [65.8, 20.0], [65.9, 20.0], [66.0, 20.0], [66.1, 20.0], [66.2, 20.0], [66.3, 20.0], [66.4, 20.0], [66.5, 21.0], [66.6, 21.0], [66.7, 21.0], [66.8, 21.0], [66.9, 21.0], [67.0, 21.0], [67.1, 21.0], [67.2, 21.0], [67.3, 21.0], [67.4, 21.0], [67.5, 21.0], [67.6, 22.0], [67.7, 22.0], [67.8, 22.0], [67.9, 22.0], [68.0, 22.0], [68.1, 22.0], [68.2, 22.0], [68.3, 23.0], [68.4, 23.0], [68.5, 23.0], [68.6, 23.0], [68.7, 23.0], [68.8, 23.0], [68.9, 23.0], [69.0, 24.0], [69.1, 24.0], [69.2, 24.0], [69.3, 24.0], [69.4, 24.0], [69.5, 24.0], [69.6, 24.0], [69.7, 25.0], [69.8, 25.0], [69.9, 25.0], [70.0, 25.0], [70.1, 25.0], [70.2, 26.0], [70.3, 26.0], [70.4, 26.0], [70.5, 26.0], [70.6, 27.0], [70.7, 27.0], [70.8, 27.0], [70.9, 27.0], [71.0, 27.0], [71.1, 27.0], [71.2, 27.0], [71.3, 28.0], [71.4, 28.0], [71.5, 28.0], [71.6, 28.0], [71.7, 29.0], [71.8, 29.0], [71.9, 30.0], [72.0, 31.0], [72.1, 31.0], [72.2, 32.0], [72.3, 35.0], [72.4, 36.0], [72.5, 36.0], [72.6, 37.0], [72.7, 37.0], [72.8, 37.0], [72.9, 38.0], [73.0, 38.0], [73.1, 40.0], [73.2, 41.0], [73.3, 41.0], [73.4, 43.0], [73.5, 46.0], [73.6, 47.0], [73.7, 47.0], [73.8, 49.0], [73.9, 50.0], [74.0, 52.0], [74.1, 53.0], [74.2, 57.0], [74.3, 57.0], [74.4, 58.0], [74.5, 59.0], [74.6, 60.0], [74.7, 60.0], [74.8, 64.0], [74.9, 65.0], [75.0, 67.0], [75.1, 70.0], [75.2, 72.0], [75.3, 75.0], [75.4, 76.0], [75.5, 78.0], [75.6, 78.0], [75.7, 79.0], [75.8, 80.0], [75.9, 80.0], [76.0, 81.0], [76.1, 83.0], [76.2, 83.0], [76.3, 83.0], [76.4, 83.0], [76.5, 83.0], [76.6, 84.0], [76.7, 84.0], [76.8, 86.0], [76.9, 95.0], [77.0, 98.0], [77.1, 101.0], [77.2, 101.0], [77.3, 103.0], [77.4, 111.0], [77.5, 113.0], [77.6, 114.0], [77.7, 114.0], [77.8, 118.0], [77.9, 119.0], [78.0, 120.0], [78.1, 121.0], [78.2, 122.0], [78.3, 123.0], [78.4, 123.0], [78.5, 130.0], [78.6, 133.0], [78.7, 138.0], [78.8, 138.0], [78.9, 139.0], [79.0, 139.0], [79.1, 140.0], [79.2, 140.0], [79.3, 142.0], [79.4, 144.0], [79.5, 144.0], [79.6, 144.0], [79.7, 146.0], [79.8, 146.0], [79.9, 146.0], [80.0, 146.0], [80.1, 147.0], [80.2, 147.0], [80.3, 148.0], [80.4, 149.0], [80.5, 150.0], [80.6, 150.0], [80.7, 152.0], [80.8, 152.0], [80.9, 155.0], [81.0, 158.0], [81.1, 159.0], [81.2, 160.0], [81.3, 160.0], [81.4, 161.0], [81.5, 161.0], [81.6, 163.0], [81.7, 164.0], [81.8, 164.0], [81.9, 165.0], [82.0, 165.0], [82.1, 166.0], [82.2, 167.0], [82.3, 167.0], [82.4, 167.0], [82.5, 168.0], [82.6, 168.0], [82.7, 168.0], [82.8, 169.0], [82.9, 172.0], [83.0, 173.0], [83.1, 173.0], [83.2, 174.0], [83.3, 174.0], [83.4, 176.0], [83.5, 177.0], [83.6, 178.0], [83.7, 178.0], [83.8, 179.0], [83.9, 180.0], [84.0, 180.0], [84.1, 181.0], [84.2, 182.0], [84.3, 182.0], [84.4, 184.0], [84.5, 185.0], [84.6, 185.0], [84.7, 186.0], [84.8, 187.0], [84.9, 187.0], [85.0, 187.0], [85.1, 187.0], [85.2, 189.0], [85.3, 189.0], [85.4, 189.0], [85.5, 189.0], [85.6, 190.0], [85.7, 191.0], [85.8, 191.0], [85.9, 193.0], [86.0, 194.0], [86.1, 196.0], [86.2, 199.0], [86.3, 202.0], [86.4, 202.0], [86.5, 203.0], [86.6, 204.0], [86.7, 204.0], [86.8, 205.0], [86.9, 205.0], [87.0, 205.0], [87.1, 206.0], [87.2, 207.0], [87.3, 207.0], [87.4, 207.0], [87.5, 207.0], [87.6, 208.0], [87.7, 208.0], [87.8, 208.0], [87.9, 208.0], [88.0, 209.0], [88.1, 209.0], [88.2, 214.0], [88.3, 216.0], [88.4, 216.0], [88.5, 216.0], [88.6, 217.0], [88.7, 217.0], [88.8, 217.0], [88.9, 217.0], [89.0, 218.0], [89.1, 219.0], [89.2, 220.0], [89.3, 220.0], [89.4, 220.0], [89.5, 220.0], [89.6, 220.0], [89.7, 220.0], [89.8, 220.0], [89.9, 221.0], [90.0, 221.0], [90.1, 221.0], [90.2, 221.0], [90.3, 221.0], [90.4, 222.0], [90.5, 222.0], [90.6, 223.0], [90.7, 223.0], [90.8, 223.0], [90.9, 223.0], [91.0, 226.0], [91.1, 226.0], [91.2, 226.0], [91.3, 226.0], [91.4, 227.0], [91.5, 227.0], [91.6, 228.0], [91.7, 230.0], [91.8, 230.0], [91.9, 231.0], [92.0, 231.0], [92.1, 231.0], [92.2, 232.0], [92.3, 233.0], [92.4, 234.0], [92.5, 234.0], [92.6, 234.0], [92.7, 235.0], [92.8, 236.0], [92.9, 236.0], [93.0, 236.0], [93.1, 237.0], [93.2, 237.0], [93.3, 238.0], [93.4, 238.0], [93.5, 238.0], [93.6, 239.0], [93.7, 239.0], [93.8, 240.0], [93.9, 240.0], [94.0, 241.0], [94.1, 241.0], [94.2, 241.0], [94.3, 243.0], [94.4, 244.0], [94.5, 244.0], [94.6, 244.0], [94.7, 244.0], [94.8, 246.0], [94.9, 246.0], [95.0, 248.0], [95.1, 249.0], [95.2, 249.0], [95.3, 250.0], [95.4, 250.0], [95.5, 251.0], [95.6, 252.0], [95.7, 253.0], [95.8, 253.0], [95.9, 254.0], [96.0, 255.0], [96.1, 255.0], [96.2, 256.0], [96.3, 257.0], [96.4, 258.0], [96.5, 260.0], [96.6, 261.0], [96.7, 263.0], [96.8, 263.0], [96.9, 264.0], [97.0, 267.0], [97.1, 269.0], [97.2, 269.0], [97.3, 277.0], [97.4, 277.0], [97.5, 279.0], [97.6, 280.0], [97.7, 282.0], [97.8, 283.0], [97.9, 286.0], [98.0, 286.0], [98.1, 286.0], [98.2, 288.0], [98.3, 289.0], [98.4, 289.0], [98.5, 291.0], [98.6, 295.0], [98.7, 298.0], [98.8, 300.0], [98.9, 303.0], [99.0, 307.0], [99.1, 307.0], [99.2, 308.0], [99.3, 309.0], [99.4, 312.0], [99.5, 313.0], [99.6, 315.0], [99.7, 318.0], [99.8, 322.0], [99.9, 323.0]], "isOverall": false, "label": "注册上报", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 12.0, "minX": 0.0, "maxY": 771.0, "series": [{"data": [[0.0, 771.0], [300.0, 12.0], [100.0, 92.0], [200.0, 125.0]], "isOverall": false, "label": "注册上报", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 300.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 1000.0, "minX": 0.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 1000.0, "series": [{"data": [[0.0, 1000.0]], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 4.9E-324, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 64.40900000000008, "minX": 1.758189E12, "maxY": 64.40900000000008, "series": [{"data": [[1.758189E12, 64.40900000000008]], "isOverall": false, "label": "b接口", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.758189E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 9.26984126984127, "minX": 1.0, "maxY": 323.0, "series": [{"data": [[2.0, 10.673913043478262], [3.0, 9.545454545454545], [4.0, 9.26984126984127], [5.0, 10.410256410256412], [6.0, 11.11864406779661], [7.0, 9.345454545454542], [8.0, 10.8], [9.0, 11.413043478260871], [10.0, 14.333333333333332], [11.0, 14.205882352941178], [12.0, 16.08823529411765], [13.0, 10.149999999999999], [14.0, 19.22222222222222], [15.0, 13.0], [16.0, 17.666666666666668], [17.0, 17.666666666666668], [18.0, 14.714285714285714], [21.0, 18.0], [22.0, 21.5], [24.0, 28.0], [25.0, 18.0], [26.0, 20.0], [28.0, 14.333333333333334], [29.0, 12.666666666666666], [30.0, 23.666666666666664], [31.0, 16.5], [35.0, 19.5], [39.0, 25.0], [38.0, 24.0], [43.0, 39.888888888888886], [42.0, 27.25], [44.0, 33.333333333333336], [47.0, 17.0], [49.0, 18.0], [51.0, 18.666666666666668], [50.0, 17.0], [53.0, 13.0], [52.0, 60.0], [58.0, 38.0], [60.0, 26.571428571428573], [61.0, 16.5], [120.0, 323.0], [159.0, 296.0], [163.0, 307.0], [162.0, 234.66666666666666], [170.0, 198.35], [186.0, 80.5], [207.0, 264.0], [206.0, 224.0], [205.0, 254.33333333333334], [204.0, 269.0], [201.0, 80.0], [202.0, 244.0], [213.0, 273.0], [211.0, 201.33333333333334], [210.0, 225.75], [209.0, 231.0], [222.0, 189.0], [221.0, 203.0], [219.0, 225.0], [218.0, 231.66666666666666], [217.0, 162.33333333333334], [226.0, 179.0], [237.0, 223.5], [244.0, 163.66666666666666], [246.0, 176.6122448979592], [247.0, 192.3644859813085], [245.0, 208.0], [240.0, 220.0], [248.0, 209.0909090909091], [1.0, 12.65]], "isOverall": false, "label": "注册上报", "isController": false}, {"data": [[64.41000000000001, 58.87999999999995]], "isOverall": false, "label": "注册上报-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 248.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 12450.0, "minX": 1.758189E12, "maxY": 14883.333333333334, "series": [{"data": [[1.758189E12, 12450.0]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.758189E12, 14883.333333333334]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.758189E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 58.87999999999995, "minX": 1.758189E12, "maxY": 58.87999999999995, "series": [{"data": [[1.758189E12, 58.87999999999995]], "isOverall": false, "label": "注册上报", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.758189E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 58.51700000000001, "minX": 1.758189E12, "maxY": 58.51700000000001, "series": [{"data": [[1.758189E12, 58.51700000000001]], "isOverall": false, "label": "注册上报", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.758189E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 22.443000000000062, "minX": 1.758189E12, "maxY": 22.443000000000062, "series": [{"data": [[1.758189E12, 22.443000000000062]], "isOverall": false, "label": "注册上报", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.758189E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 4.0, "minX": 1.758189E12, "maxY": 323.0, "series": [{"data": [[1.758189E12, 323.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.758189E12, 221.0]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.758189E12, 306.96000000000004]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.758189E12, 247.89999999999986]], "isOverall": false, "label": "95th percentile", "isController": false}, {"data": [[1.758189E12, 4.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.758189E12, 12.0]], "isOverall": false, "label": "Median", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.758189E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 9.0, "minX": 254.0, "maxY": 207.0, "series": [{"data": [[345.0, 9.0], [401.0, 10.0], [254.0, 207.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 401.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 9.0, "minX": 254.0, "maxY": 205.5, "series": [{"data": [[345.0, 9.0], [401.0, 10.0], [254.0, 205.5]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 401.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 16.666666666666668, "minX": 1.758189E12, "maxY": 16.666666666666668, "series": [{"data": [[1.758189E12, 16.666666666666668]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.758189E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 16.666666666666668, "minX": 1.758189E12, "maxY": 16.666666666666668, "series": [{"data": [[1.758189E12, 16.666666666666668]], "isOverall": false, "label": "200", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.758189E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 16.666666666666668, "minX": 1.758189E12, "maxY": 16.666666666666668, "series": [{"data": [[1.758189E12, 16.666666666666668]], "isOverall": false, "label": "注册上报-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.758189E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 16.666666666666668, "minX": 1.758189E12, "maxY": 16.666666666666668, "series": [{"data": [[1.758189E12, 16.666666666666668]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.758189E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

