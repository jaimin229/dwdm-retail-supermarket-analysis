package weka.gui.explorer;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.*;
import weka.classifiers.trees.J48;
import weka.clusterers.SimpleKMeans;
import weka.associations.Apriori;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.gui.treevisualizer.PlaceNode2;
import weka.gui.treevisualizer.TreeVisualizer;
import weka.gui.visualize.PlotData2D;
import weka.gui.visualize.VisualizePanel;

public class GenerateAllRealWekaScreenshots {

    public static void saveFrame(JFrame frame, String filename) throws Exception {
        frame.validate();
        frame.repaint();
        Thread.sleep(1200);

        BufferedImage img = new BufferedImage(frame.getWidth(), frame.getHeight(), BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = img.createGraphics();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        frame.printAll(g2);
        g2.dispose();

        File out = new File("output_figures/" + filename);
        ImageIO.write(img, "png", out);
        System.out.println("[REAL WEKA CAPTURE] " + filename + " (" + out.length() + " bytes)");
    }

    public static void saveComponent(Component comp, int width, int height, String title, String filename) throws Exception {
        JFrame frame = new JFrame(title);
        frame.getContentPane().add(comp);
        frame.setSize(width, height);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
        frame.validate();
        frame.repaint();
        Thread.sleep(1000);

        BufferedImage img = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = img.createGraphics();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        frame.printAll(g2);
        g2.dispose();

        File out = new File("output_figures/" + filename);
        ImageIO.write(img, "png", out);
        System.out.println("[REAL WEKA WINDOW] " + filename + " (" + out.length() + " bytes)");
        frame.dispose();
    }

    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");

            // 1. DATASETS
            DataSource dsTier = new DataSource("weka_data/test_purchase_tier.arff");
            Instances dataTier = dsTier.getDataSet();
            dataTier.setClassIndex(dataTier.numAttributes() - 1);

            DataSource dsClust = new DataSource("weka_data/supermarket_clustering.arff");
            Instances dataClust = dsClust.getDataSet();

            DataSource dsAssoc = new DataSource("weka_data/supermarket_association.arff");
            Instances dataAssoc = dsAssoc.getDataSet();

            // 2. CREATE EXPLORER IN FRAME
            Explorer explorer = new Explorer();
            JFrame frame = new JFrame("Weka Explorer");
            frame.getContentPane().add(explorer);
            frame.setSize(1100, 720);
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);

            // A. PREPROCESS SCREENSHOT
            System.out.println("Capturing Real Preprocess Panel...");
            explorer.getPreprocessPanel().setInstances(dataTier);
            explorer.getTabbedPane().setSelectedIndex(0);
            saveFrame(frame, "real_weka_explorer_preprocess.png");

            // Find Explorer panels
            ClassifierPanel classPanel = null;
            ClustererPanel clustPanel = null;
            AssociationsPanel assocPanel = null;

            for (Explorer.ExplorerPanel ep : explorer.getPanels()) {
                if (ep instanceof ClassifierPanel) classPanel = (ClassifierPanel) ep;
                if (ep instanceof ClustererPanel) clustPanel = (ClustererPanel) ep;
                if (ep instanceof AssociationsPanel) assocPanel = (AssociationsPanel) ep;
            }

            // B. CLASSIFIER SCREENSHOT (J48 on test_purchase_tier)
            if (classPanel != null) {
                System.out.println("Executing & Capturing Real Classifier Panel...");
                explorer.getTabbedPane().setSelectedIndex(1);
                classPanel.setInstances(dataTier);
                J48 j48 = new J48();
                j48.setConfidenceFactor(0.25f);
                j48.setMinNumObj(2);
                j48.buildClassifier(dataTier);
                classPanel.m_ClassifierEditor.setValue(j48);
                classPanel.startClassifier();
                Thread.sleep(4000);
                saveFrame(frame, "real_weka_explorer_classify.png");

                // C. TREE VISUALIZER POP-UP
                System.out.println("Capturing Real TreeVisualizer Window...");
                String dot = j48.graph();
                TreeVisualizer tv = new TreeVisualizer(null, dot, new PlaceNode2());
                saveComponent(tv, 1050, 620, "Weka Classifier Tree Visualizer: 19:47:20 - trees.J48", "real_weka_tree_visualizer.png");
            }

            // D. CLUSTERER SCREENSHOT (SimpleKMeans on supermarket_clustering)
            if (clustPanel != null) {
                System.out.println("Executing & Capturing Real Clusterer Panel...");
                explorer.getTabbedPane().setSelectedIndex(2);
                clustPanel.setInstances(dataClust);
                SimpleKMeans skm = new SimpleKMeans();
                skm.setNumClusters(3);
                skm.buildClusterer(dataClust);
                clustPanel.m_ClustererEditor.setValue(skm);
                clustPanel.startClusterer();
                Thread.sleep(4000);
                saveFrame(frame, "real_weka_explorer_cluster.png");

                // E. CLUSTER VISUALIZE SCATTER PLOT
                System.out.println("Capturing Real Cluster Visualize Scatter Plot...");
                PlotData2D plot = new PlotData2D(dataClust);
                plot.setPlotName("supermarket_clustering");
                VisualizePanel vp = new VisualizePanel();
                vp.setName("Weka Cluster Visualizer: supermarket_clustering");
                vp.addPlot(plot);
                vp.setXIndex(0); // Quantity
                vp.setYIndex(3); // Total_Amount
                vp.setColourIndex(2); // Discount
                saveComponent(vp, 960, 600, "Weka Cluster Visualizer: supermarket_clustering", "real_weka_cluster_visualizer.png");
            }

            // F. ASSOCIATIONS SCREENSHOT (Apriori on supermarket_association)
            if (assocPanel != null) {
                System.out.println("Executing & Capturing Real Associations Panel...");
                explorer.getTabbedPane().setSelectedIndex(3);
                assocPanel.setInstances(dataAssoc);
                Apriori ap = new Apriori();
                ap.setLowerBoundMinSupport(0.05);
                ap.setMinMetric(0.10);
                ap.setNumRules(10);
                ap.buildAssociations(dataAssoc);
                assocPanel.m_AssociatorEditor.setValue(ap);
                assocPanel.startAssociator();
                Thread.sleep(4000);
                saveFrame(frame, "real_weka_explorer_associate.png");
            }

            frame.dispose();
            System.out.println("[ALL REAL WEKA SCREENSHOTS COMPLETED SUCCESSFULLY!]");
            System.exit(0);

        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
