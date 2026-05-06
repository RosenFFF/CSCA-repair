<template>
  <div class="chart-container">
    <h3 class="chart-title">每周报名趋势</h3>
    <v-chart :option="chartOption" autoresize style="height: 240px" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const props = defineProps({ trend: Array })

const chartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderColor: '#eee',
    textStyle: { color: '#333', fontSize: 12 },
  },
  legend: {
    data: ['第一班次', '第二班次'],
    bottom: 0,
    textStyle: { color: '#999', fontSize: 11 },
    itemWidth: 12,
    itemHeight: 8,
    itemGap: 16,
  },
  grid: { left: 36, right: 12, top: 12, bottom: 36 },
  xAxis: {
    type: 'category',
    data: props.trend?.map((t) => {
      const d = new Date(t.date)
      return `${d.getMonth() + 1}/${d.getDate()}`
    }) || [],
    axisLine: { lineStyle: { color: '#eee' } },
    axisLabel: { color: '#999', fontSize: 11 },
    axisTick: { show: false },
  },
  yAxis: {
    type: 'value',
    minInterval: 1,
    splitLine: { lineStyle: { color: '#f5f5f5' } },
    axisLabel: { color: '#bbb', fontSize: 11 },
  },
  series: [
    {
      name: '第一班次',
      type: 'bar',
      data: props.trend?.map((t) => t.shift1) || [],
      barWidth: '28%',
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#764ba2' },
          ],
        },
        borderRadius: [4, 4, 0, 0],
      },
    },
    {
      name: '第二班次',
      type: 'bar',
      data: props.trend?.map((t) => t.shift2) || [],
      barWidth: '28%',
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#13c2c2' },
            { offset: 1, color: '#667eea' },
          ],
        },
        borderRadius: [4, 4, 0, 0],
      },
    },
  ],
}))
</script>

<style scoped>
.chart-container {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}
.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 8px;
}
</style>
