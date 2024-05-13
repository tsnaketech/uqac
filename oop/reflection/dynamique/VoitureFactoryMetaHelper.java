package dynamique;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.tools.Diagnostic;
import javax.tools.DiagnosticCollector;
import javax.tools.FileObject;
import javax.tools.ForwardingJavaFileManager;
import javax.tools.JavaCompiler;
import javax.tools.JavaFileManager;
import javax.tools.JavaFileObject;
import javax.tools.ToolProvider;

import voiture.Voiture;

public class VoitureFactoryMetaHelper {
	
		private static String nameClass;
		private static StringBuilder sb;
		private static JavaCompiler compiler;
		private static JavaFileManager fileManager;
		private static DiagnosticCollector<JavaFileObject> collector;
		private static List<ByteArrayClass> classes;
		private static List<JavaFileObject> sources;
		private static Voiture voiture;
		
		public static Voiture generationMetaVoiture(boolean sportive, int vitesse, int id) {
			voiture = null;
			
			manager();
			sb = genererClass(sportive, id);
			source(nameClass, sb);
			compile();
			instanciation(nameClass, sportive, vitesse);
			return voiture;
		}

		private static void manager() {
            compiler = ToolProvider.getSystemJavaCompiler();
            classes = new ArrayList<>();
            collector = new DiagnosticCollector<JavaFileObject>();

            fileManager = compiler.getStandardFileManager(null, null, null);

            // La classe qui se charge de fournir les "conteneurs" au compilateur
            fileManager = new ForwardingJavaFileManager<JavaFileManager>(fileManager){
                public JavaFileObject getJavaFileForOutput(Location location, String className, JavaFileObject.Kind kind,
                                                           FileObject sibling) throws IOException{
                    if (kind == JavaFileObject.Kind.CLASS){
                        ByteArrayClass outFile = new ByteArrayClass(className);
                        classes.add(outFile);
                        return outFile;
                    }
                    else
                        return super.getJavaFileForOutput(location, className, kind, sibling);
                }
            };
            
		}
		
		private static void source(String name, StringBuilder sb) {
			JavaFileObject meta = new StringSource(name, sb.toString());
            sources = Arrays.asList(meta);
		}
		
		private static void compile() {
            JavaCompiler.CompilationTask task = compiler.getTask(null, fileManager, collector, null,
                    null, sources);
            Boolean result = task.call();

            for (Diagnostic<? extends JavaFileObject> d : collector.getDiagnostics())
                System.out.println(d);

            try {
                fileManager.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            if (!result) {
                System.out.println("ECHEC DE LA COMPILATION");
                System.exit(1);
            }
		}
		
		private static void instanciation(String name,boolean sportive, int vitesse) {
            ByteArrayClasseLoader loader = new ByteArrayClasseLoader(classes);
            try {
	        	if (sportive) {
	        		voiture = (Voiture)(Class.forName("dynamique."+name, true, loader).getDeclaredConstructor().newInstance());
	        	} else {
	        		voiture = (Voiture)(Class.forName("dynamique."+name, true, loader).getDeclaredConstructor(int.class).newInstance(vitesse));
	        	}
			} catch (InstantiationException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalArgumentException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (InvocationTargetException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (NoSuchMethodException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SecurityException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
            
		}
		
		private static StringBuilder genererClass(boolean sportive, int id) { 
			String name = null;
			StringBuilder sb = new StringBuilder();
	    	sb.append("package dynamique;\n\n");
        	if (!sportive) {
        		name = "MetaVoiture";
        		genererImport(sb, "Voiture");
        		genererName(sb, name,"Voiture");
        		genererConstructeurs(sb, name);
        		genererMethodes(sb);     		
        	} else {
        		name = "MetaVoitureSport";
        		genererImport(sb, "VoitureSport");
        		genererName(sb, name,"VoitureSport");
        		genererMethodes(sb);
        	}
        	sb.append("}");
        	nameClass = name;
        	printClass(sb, name);
        	return sb;
		}

	    private static void genererImport(StringBuilder sb, String extend) {

        	sb.append("import voiture."+extend+";\n");
        	sb.append("import voiture.Surveillable;\n\n");

	    }
	    
	    private static void genererName(StringBuilder sb, String name, String extend) {

	    	sb.append("public class " + name + " extends " + extend + " implements Surveillable {\n\n");

	    }
		
	    private static void genererConstructeurs(StringBuilder sb, String name) {
	    	sb.append(" public "+name+"(int vitesse){\n" + 
 				   	  " 	super(vitesse);\n" + 
 				      " }\n\n");
	    }
	    
	    private static void genererMethodes(StringBuilder sb) {

        	sb.append("@Override\n"+
    	            " public int surveiller(int limite){\n"+
    	            " 	return vitesse - limite;\n"+
    	            " }\n");

	    }
	    
	    private static void printClass(StringBuilder sb, String name) {
            System.out.println("#### La classe " + name + " ####");
            System.out.println(sb.toString());
	    }
}
