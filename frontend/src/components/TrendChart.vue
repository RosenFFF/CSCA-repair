<template>
  <div class="chart-container">
    <h3 class="chart-title">每周报名趋势</h3>
    <v-chart :option="chartOption" autoresize style="height: 250px" />
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
  tooltip: { trigger: 'axis' },
  legend: { data: ['第一班', '第二班'], bottom: 0 },
  grid: { left: 40, right: 16, top: 16, bottom: 40 },
  xAxis: {
    type: 'category',
    data: props.trend?.map((t) => {
      const d = new Date(t.date)
      return `${d.getMonth() + 1}/${d.getDate()}`
    }) || [],
  },
  yAxis: { type: 'value', minInterval: 1 },
  series: [
    {
      name: '第一班',
      type: 'bar',
      data: props.trend?.map((t) => t.shift1) || [],
      itemStyle: { color: '#1890ff', borderRadius: [4, 4, 0, 0] },
    },
    {
      name: '第二班',
      type: 'bar',
      data: props.trend?.map((t) => t.shift2) || [],
      itemStyle: { color: '#13c2c2', borderRadius: [4, 4, 0, 0] },
    },
  ],
}))
</script>

<style scoped>
.chart-container {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.chart-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
}
</style>
