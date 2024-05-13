package oracle;

public class Oracle {

	private static Oracle instance;
    private Council council;
    private Judgement judgement;
    private Listen listen;
    private Miracle miracle;
	
    private Oracle() {
    	this.council = new Council();
    	this.judgement = new Judgement();
    	this.listen = new Listen();
    	this.miracle = new Miracle();
    }
    
    public static Oracle getInstance() {
        if(instance == null) {
        	instance = new Oracle();
        }
        return instance;
    }
    
    void print(String s) {

        System.out.println(s);
    }
    
    public CouncilInterface getCouncilInterface() {
        return (CouncilInterface)council;
    }
    
    public JudgementInterface getJudgementInterface() {
        return (JudgementInterface)judgement;
    }
    
    public ListenInterface getListenInterface() {
        return (ListenInterface)listen;
    }
    
    public MiracleInterface getMiracleInterface() {
        return (MiracleInterface)miracle;
    }
    
    Council getCouncil() {
        return council;
    }
    
    Judgement getJudgement() {
        return judgement;
    }
    
    Listen getListen() {
        return listen;
    }
    
    Miracle getMiracle() {
        return miracle;
    }
    
}
