import { useMemo } from 'react';
import { Card } from '@/components/ui/card';
// Grafik için Recharts ve UI bileşenlerini içe aktar
import { Pie, PieChart, Cell, Tooltip, Legend } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
  type ChartConfig
} from "@/components/ui/chart";

interface ClassificationResultProps {
  imageBase64: string;
  objectCount: number;
  classCounts: Record<string, number>;
}

// Grafiğimizdeki her sınıf için bir renk tanımlayalım.
// Bu renkler temanızdaki (src/index.css) CSS değişkenlerinden gelir.
const chartConfig = {
  Yıldız: { label: "Yıldız", color: "hsl(var(--primary))" }, // Mavi
  Bulutsu: { label: "Bulutsu", color: "hsl(var(--accent))" }, // Turuncu
  Galaksi: { label: "Galaksi", color: "hsl(271 91% 65%)" }, // Mor
  "Kuyruklu Yıldız": { label: "Kuyruklu Yıldız", color: "hsl(120 71% 50%)" }, // Yeşil
  Gezegen: { label: "Gezegen", color: "hsl(180 71% 50%)" }, // Camgöbeği
  Gürültü: { label: "Gürültü", color: "hsl(var(--destructive))" }, // Kırmızı
  // Bilinmeyen bir sınıf gelirse diye bir yedek renk
  default: { label: "Diğer", color: "hsl(var(--muted-foreground))" }
} satisfies ChartConfig;

export const ClassificationResult = ({ 
  imageBase64, 
  objectCount, 
  classCounts 
}: ClassificationResultProps) => {

  // Recharts, { "Yıldız": 355 } gibi bir obje yerine
  // [{ name: "Yıldız", count: 355, fill: "hsl(...)" }] gibi bir dizi bekler.
  // Bu useMemo hook'u, classCounts her değiştiğinde bu dönüşümü yapar.
  const chartData = useMemo(() => {
    // Sınıfları, 'chartConfig'da tanımladığımız sıraya göre sıralamak
    // ve bilinmeyenleri sona eklemek için:
    const classOrder = Object.keys(chartConfig);
    
    const sortedEntries = Object.entries(classCounts).sort(([aName], [bName]) => {
      const aIndex = classOrder.indexOf(aName);
      const bIndex = classOrder.indexOf(bName);
      // Bilinmeyen sınıfları sona at
      if (aIndex === -1) return 1;
      if (bIndex === -1) return -1;
      return aIndex - bIndex;
    });

    return sortedEntries.map(([name, count]) => ({
      name: name,
      count: count,
      // Renk atamasını config'den yap, bulunamazsa varsayılanı kullan
      fill: (chartConfig[name as keyof typeof chartConfig] || chartConfig.default).color,
    }));
  }, [classCounts]);

  return (
    <div className="grid md:grid-cols-2 gap-8 mt-12 animate-in fade-in duration-700">
      <Card className="p-6 space-y-4 bg-card border-border shadow-glow">
        <h2 className="text-2xl font-bold text-foreground">İşlenmiş Görüntü</h2>
        <div className="rounded-lg overflow-hidden bg-secondary/30 p-2">
          <img
            src={`data:image/jpeg;base64,${imageBase64}`}
            alt="Processed astronomical image"
            className="w-full h-auto rounded-lg"
          />
        </div>
      </Card>

      <Card className="p-6 space-y-6 bg-card border-border shadow-glow">
        <h2 className="text-2xl font-bold text-foreground">Sınıflandırma Özeti</h2>
        
        <div className="space-y-4">
          <div className="p-4 rounded-lg bg-primary/10 border border-primary/20">
            <p className="text-sm text-muted-foreground mb-1">Tespit Edilen Nesne Sayısı</p>
            <p className="text-4xl font-bold text-primary">{objectCount}</p>
          </div>

          <div className="space-y-3">
            <h3 className="text-lg font-semibold text-foreground">Sınıf Dağılımı</h3>
            
            {chartData.length > 1 && (
              <div className="h-[250px] w-full">
                <ChartContainer config={chartConfig} className="h-full w-full">
                  <PieChart>
                    <Tooltip 
                      cursor={false} 
                      content={<ChartTooltipContent 
                        indicator="dot" 
                        labelClassName="font-medium capitalize"
                        nameKey="name"
                        className="bg-card border-border shadow-glow" 
                      />} 
                    />
                    <Pie
                      data={chartData}
                      dataKey="count"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      innerRadius="60%"
                      outerRadius="80%"
                      paddingAngle={2}
                      labelLine={false}
                      label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                    >
                      {chartData.map((entry) => (
                        <Cell key={`cell-${entry.name}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Legend 
                      content={<ChartLegendContent 
                        nameKey="name"
                        className="text-muted-foreground capitalize"
                      />} 
                      verticalAlign="bottom"
                      wrapperStyle={{ paddingTop: 10, paddingBottom: 10 }}
                    />
                  </PieChart>
                </ChartContainer>
              </div>
            )}

            {/* --- GÜNCELLENMİŞ LİSTE GÖRÜNÜMÜ --- */}
            {chartData.length <= 1 && (
              <h4 className="text-sm font-medium text-muted-foreground">Sayılar:</h4>
            )}
            <div className="space-y-2">
              {chartData.map(({ name, count, fill }) => (
                <div 
                  key={name}
                  className="flex items-center justify-between p-3 rounded-lg bg-secondary/50 border border-border hover:bg-secondary/70 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    {/* Renk noktası */}
                    <div 
                      className="h-3 w-3 rounded-full" 
                      style={{ backgroundColor: fill }} 
                    />
                    <span className="text-foreground font-medium capitalize">{name}</span>
                  </div>
                  <span className="text-2xl font-bold text-foreground" style={{ color: fill }}>
                    {count}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};