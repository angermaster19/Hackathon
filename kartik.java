import java.util.*;

public class Main {
    public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int n = scan.nextInt();
		scan.nextLine();
		String s = scan.nextLine();
		int a = MaxPerfect(s,n,'a');
		int b = MaxPerfect(s,n,'b');
		System.out.print(Math.max(a,b));
	}

	// aaaabababbaaabba k=2

	public static int MaxPerfect(String s, int k, char ch){
		int si=0,ei=0,ans=0,flip=0; ///

		//grow
		while(ei<s.length()){
			if(s.charAt(ei)!=ch){
				flip++; 
			}

			//shrink
			while(flip>k){
				if(s.charAt(si)!=ch){
					flip--;
				}
				si++;
			}


			//update
			ans = Math.max(ans,ei-si+1);
			ei++;
		}
		return ans;
	}
}
